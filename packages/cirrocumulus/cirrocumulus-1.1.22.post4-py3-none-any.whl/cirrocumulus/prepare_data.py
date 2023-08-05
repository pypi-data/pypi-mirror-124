import argparse
import logging
import os

import anndata
import numpy as np
import pandas as pd
import scipy.sparse

from cirrocumulus.anndata_util import get_scanpy_marker_keys, datasets_schema, ADATA_MODULE_UNS_KEY
from cirrocumulus.io_util import get_markers, filter_markers, add_spatial, SPATIAL_HELP, unique_id
from cirrocumulus.util import to_json, get_fs

logger = logging.getLogger("cirro")

cluster_fields = ['anno', 'cell_type', 'celltype', 'leiden', 'louvain', 'seurat_cluster', 'cluster']
categorical_fields_convert = ['seurat_clusters']


def read_adata(path, backed=False, spatial_directory=None, use_raw=False):
    if path.lower().endswith('.loom'):
        adata = anndata.read_loom(path)
    elif path.lower().endswith('.zarr'):
        adata = anndata.read_zarr(path)
    else:
        adata = anndata.read(path, backed=backed)
    if 'module' in adata.uns:
        adata.uns[ADATA_MODULE_UNS_KEY] = anndata.AnnData(X=adata.uns['module']['X'],
                                                          var=adata.uns['module']['var'])
    if use_raw and adata.raw is not None and adata.shape[0] == adata.raw.shape[0]:
        logger.info('Using adata.raw')
        adata = anndata.AnnData(X=adata.raw.X, var=adata.raw.var, obs=adata.obs, obsm=adata.obsm, uns=adata.uns)

    if spatial_directory is not None:
        if not add_spatial(adata, spatial_directory):
            logger.info('No spatial data found in {}'.format(spatial_directory))

    def fix_column_names(df):
        rename = {}
        for c in df.columns:
            if c.find(' ') != -1:
                rename[c] = c.replace(' ', '_')
        return df.rename(rename, axis=1) if len(rename) > 0 else df

    adata.obs = fix_column_names(adata.obs)
    adata.var = fix_column_names(adata.var)
    for field in categorical_fields_convert:
        if field in adata.obs and not pd.api.types.is_categorical_dtype(adata.obs[field]):
            logger.info('Converting {} to categorical'.format(field))
            adata.obs[field] = adata.obs[field].astype('category')
    for key in adata.obsm:
        if key.find(' ') != -1:
            new_key = key.replace(' ', '_')
            adata.obsm[new_key] = adata.obsm[key]
            del adata.obsm[key]
    if not backed and scipy.sparse.issparse(adata.X) and scipy.sparse.isspmatrix_csr(adata.X):
        adata.X = adata.X.tocsc()
    return adata


#
# def make_unique(index, join='-1'):
#     index = index.str.replace('/', '_')
#     lower_index = index.str.lower()
#     if lower_index.is_unique:
#         return index
#     from collections import defaultdict
#
#     indices_dup = lower_index.duplicated(keep="first")
#     values_dup_lc = lower_index.values[indices_dup]
#     values_dup = index.values[indices_dup]
#     counter = defaultdict(lambda: 0)
#     for i, v in enumerate(values_dup_lc):
#         counter[v] += 1
#         values_dup[i] += join + str(counter[v])
#     values = index.values
#     values[indices_dup] = values_dup
#     index = pd.Index(values)
#     return index


class PrepareData:

    def __init__(self, datasets, output, dimensions=None, groups=[], group_nfeatures=10, markers=[],
                 output_format='parquet', no_auto_groups=False, save_whitelist=None):
        self.datasets = datasets
        self.groups = groups
        self.group_nfeatures = group_nfeatures
        self.markers = markers
        self.output_format = output_format
        self.no_auto_groups = no_auto_groups
        self.save_whitelist = save_whitelist

        for dataset in datasets:
            for key in list(dataset.obsm.keys()):
                m = dataset.obsm[key]
                dim = m.shape[1]
                if not (1 < dim <= 3):
                    del dataset.obsm[key]
        data_type2_datasets = {}
        for i in range(len(datasets)):
            dataset = datasets[i]
            if i > 0:
                name = dataset.uns.get('name', 'dataset {}'.format(i + 1))
                prefix = name + '-'
                dataset.var.index = prefix + dataset.var.index.astype(str)
                # ensure cell ids are the same
                if not np.array_equal(datasets[0].obs.index, dataset.obs.index):
                    raise ValueError('{} obs ids are not equal'.format(name))
            data_type = dataset.uns.get('experiment_type')

            dataset_list = data_type2_datasets.get(data_type)
            if dataset_list is None:
                dataset_list = []
                data_type2_datasets[data_type] = dataset_list
            dataset_list.append(dataset)
        datasets = []
        for data_type in data_type2_datasets:
            dataset_list = data_type2_datasets[data_type]
            dataset = anndata.concat(dataset_list, axis=1) if len(dataset_list) > 1 else dataset_list[0]
            dataset.var.index = dataset.var.index.str.replace('/', '_')
            dataset.var_names_make_unique()
            dataset.obs.index.name = 'index'
            dataset.var.index.name = 'index'
            datasets.append(dataset)
        primary_dataset = datasets[0]
        for i in range(1, len(datasets)):
            dataset = datasets[i]
            # mark duplicate in obs, then delete after computing DE
            obs_duplicates = []
            dataset.uns['cirro_obs_delete'] = obs_duplicates
            for key in list(dataset.obs.keys()):
                if key in primary_dataset.obs.columns and dataset.obs[key].equals(primary_dataset.obs[key]):
                    obs_duplicates.append(key)
                else:
                    dataset.obs[prefix + key] = dataset.obs[key]
                    del dataset.obs[key]

            for key in list(dataset.obsm.keys()):
                if key in primary_dataset.obsm and np.array_equal(dataset.obsm[key], primary_dataset.obsm[key]):
                    del dataset.obsm[key]
                else:
                    dataset.obsm[prefix + key] = dataset.obsm[key]  # rename
                    del dataset.obsm[key]

        self.base_output = output
        dimensions_supplied = dimensions is not None and len(dimensions) > 0
        self.dimensions = [] if not dimensions_supplied else dimensions
        self.measures = []
        self.others = []
        for dataset in datasets:
            for i in range(len(dataset.obs.columns)):
                name = dataset.obs.columns[i]
                c = dataset.obs[name]
                if pd.api.types.is_object_dtype(c):
                    dataset.obs[name] = dataset.obs[name].astype('category')
                    c = dataset.obs[name]
                if not dimensions_supplied and pd.api.types.is_categorical_dtype(c):
                    if 1 < len(c.cat.categories) < 2000:
                        self.dimensions.append(name)
                        if c.isna().sum() > 0:
                            logger.info('Replacing nans in {}'.format(name))
                            dataset.obs[name] = dataset.obs[name].astype(str)
                            dataset.obs.loc[dataset.obs[name].isna(), name] = ''
                            dataset.obs[name] = dataset.obs[name].astype('category')
                    else:
                        self.others.append(name)
                elif not pd.api.types.is_string_dtype(c) and not pd.api.types.is_object_dtype(c):
                    self.measures.append('obs/' + name)
                else:
                    self.others.append(name)

    def execute(self):
        output_format = self.output_format
        if self.groups is None and not self.no_auto_groups:
            groups = []
            for dataset in self.datasets:
                existing_fields = set()
                scanpy_marker_keys = get_scanpy_marker_keys(dataset)
                for key in scanpy_marker_keys:
                    existing_fields.add(dataset.uns[key]['params']['groupby'])
                for field in dataset.obs.columns:
                    field_lc = field.lower()
                    for cluster_field in cluster_fields:
                        if field_lc.find(cluster_field) != -1 and cluster_field not in existing_fields:
                            groups.append(field)
                            break
            self.groups = groups
        if self.groups is not None and len(self.groups) > 0:
            use_pegasus = False
            use_scanpy = False
            try:
                import pegasus as pg
                use_pegasus = True
            except ModuleNotFoundError:
                pass
            if not use_pegasus:
                try:
                    import scanpy as sc
                    use_scanpy = True
                except ModuleNotFoundError:
                    pass
            if not use_pegasus and not use_scanpy:
                raise ValueError('Please install pegasuspy or scanpy to compute markers')
            for dataset in self.datasets:
                for group in self.groups:
                    field = group
                    if group not in dataset.obs:  # test if multiple comma separated fields
                        split_groups = group.split(',')
                        if len(split_groups) > 1:
                            use_split_groups = True
                            for split_group in split_groups:
                                if split_group not in dataset.obs:
                                    use_split_groups = False
                                    break
                            if use_split_groups:
                                dataset.obs[field] = dataset.obs[split_groups[0]].str.cat(dataset.obs[split_groups[1:]],
                                                                                          sep=',')

                    if field in dataset.obs:
                        if not pd.api.types.is_categorical_dtype(dataset.obs[field]):
                            dataset.obs[field] = dataset.obs[field].astype('category')
                        if len(dataset.obs[field].cat.categories) > 1:
                            print('Computing markers for {}'.format(field))
                            key_added = 'rank_genes_' + str(field)
                            if use_pegasus:
                                pg.de_analysis(dataset, cluster=field, de_key=key_added)
                            else:
                                sc.tl.rank_genes_groups(dataset, field, key_added=key_added, method='t-test')
        # remove duplicate obs fields after DE
        for dataset in self.datasets:
            obs_duplicates = dataset.uns.get('cirro_obs_delete', [])
            for key in obs_duplicates:
                del dataset.obs[key]

        schema = self.get_schema()
        schema['format'] = output_format
        if output_format in ['parquet', 'zarr']:
            output_dir = self.base_output
        else:
            output_dir = os.path.splitext(self.base_output)[0]
        filesystem = get_fs(output_dir)
        filesystem.makedirs(output_dir, exist_ok=True)
        results = schema.get('results', [])

        if len(results) > 0:
            uns_dir = os.path.join(output_dir, 'uns')
            is_gzip = output_format != 'jsonl'
            filesystem.makedirs(uns_dir, exist_ok=True)

            for i in range(len(results)):
                full_result = results[i]
                result_id = full_result.pop('id')
                # keep id, name, type in schema, store rest in file
                results[i] = dict(id=result_id, name=full_result.pop('name'), type=full_result.pop('type'),
                                  content_type='application/json', content_encoding='gzip' if is_gzip else None)

                result_path = os.path.join(uns_dir, result_id + '.json.gz') if is_gzip else os.path.join(uns_dir,
                                                                                                         result_id + '.json')
                with filesystem.open(result_path, 'wt', compression='gzip' if is_gzip else None) as out:
                    out.write(to_json(full_result))

        for dataset in self.datasets:
            images = dataset.uns.get('images')
            if images is not None:
                image_dir = os.path.join(output_dir, 'images')
                filesystem.makedirs(image_dir, exist_ok=True)
                for image in images:
                    src = image['image']
                    dest = os.path.join(image_dir, os.path.basename(src))
                    filesystem.copy(src, dest)
                    image['image'] = 'images/' + os.path.basename(src)

        if output_format == 'parquet':
            from cirrocumulus.parquet_output import save_datasets_pq
            save_datasets_pq(self.datasets, schema, self.base_output, filesystem, self.save_whitelist)
        elif output_format == 'jsonl':
            from cirrocumulus.jsonl_io import save_datasets_jsonl
            save_datasets_jsonl(self.datasets, schema, output_dir, self.base_output, filesystem)
        elif output_format == 'zarr':
            from cirrocumulus.zarr_output import save_datasets_zarr
            save_datasets_zarr(self.datasets, schema, self.base_output, filesystem, self.save_whitelist)
        elif output_format == 'h5ad':
            from cirrocumulus.h5ad_output import save_datasets_h5ad
            save_datasets_h5ad(self.datasets, schema, self.base_output, filesystem, self.save_whitelist)
        else:
            raise ValueError("Unknown format")

    def get_schema(self):
        result = datasets_schema(self.datasets)
        markers = result.get('markers', [])

        if self.markers is not None:  # add results specified from file
            markers += get_markers(self.markers)
            markers = filter_markers(self.datasets[0], markers)  # TODO check if markers are in union of all features

        for marker in markers:
            if marker.get('id') is None:
                marker['id'] = unique_id()
            marker['readonly'] = True
        result['markers'] = markers
        result['format'] = self.output_format
        return result


def main(argsv):
    parser = argparse.ArgumentParser(
        description='Prepare a dataset for cirrocumulus server.')
    parser.add_argument('dataset', help='Path to a h5ad, loom, or Seurat file', nargs='+')
    parser.add_argument('--out', help='Path to output directory')
    parser.add_argument('--format', help='Output format', choices=['parquet', 'jsonl', 'zarr'],
                        default='parquet')
    parser.add_argument('--whitelist',
                        help='Optional whitelist of fields to save. Only applies when output format is parquet',
                        choices=['obs', 'obsm', 'X'],
                        action='append')
    parser.add_argument('--backed', help='Load h5ad file in backed mode', action='store_true')
    parser.add_argument('--markers',
                        help='Path to JSON file of precomputed markers that maps name to features. For example {"a":["gene1", "gene2"], "b":["gene3"]',
                        action='append')
    parser.add_argument('--no-auto-groups', dest='no_auto_groups',
                        help='Disable automatic cluster field detection to compute differential expression results for',
                        action='store_true')
    parser.add_argument('--groups',
                        help='List of groups to compute markers for (e.g. louvain). Note that markers created with scanpy or cumulus are automatically included.',
                        action='append')
    parser.add_argument('--group_nfeatures', help='Number of marker genes/features to include', type=int, default=10)
    parser.add_argument('--spatial', help=SPATIAL_HELP)
    args = parser.parse_args(argsv)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    out = args.out
    no_auto_groups = args.no_auto_groups
    save_whitelist = args.whitelist
    input_datasets = args.dataset  # multimodal
    output_format = args.format
    if out is None:
        out = os.path.splitext(os.path.basename(input_datasets[0]))[0]
    if out.endswith('/'):
        out = out[:len(out) - 1]
    output_format2extension = dict(parquet='.cpq', jsonl='.jsonl', zarr='.zarr', h5ad='.h5ad')
    if not out.lower().endswith(output_format2extension[output_format]):
        out += output_format2extension[output_format]

    datasets = []
    tmp_files = []
    for input_dataset in input_datasets:
        use_raw = False
        if input_dataset.lower().endswith('.rds'):
            import subprocess
            import tempfile
            import pkg_resources

            _, h5_file = tempfile.mkstemp(suffix='.h5ad')
            os.remove(h5_file)
            subprocess.check_call(
                ['Rscript', pkg_resources.resource_filename("cirrocumulus", 'seurat2h5ad.R'), input_dataset, h5_file])
            input_dataset = h5_file
            tmp_file = h5_file
            use_raw = True
            tmp_files.append(tmp_file)
        adata = read_adata(input_dataset, backed=args.backed, spatial_directory=args.spatial, use_raw=use_raw)
        datasets.append(adata)
        adata.uns['name'] = os.path.splitext(os.path.basename(input_dataset))[0]

    prepare_data = PrepareData(datasets=datasets, output=out, dimensions=args.groups, groups=args.groups,
                               group_nfeatures=args.group_nfeatures,
                               markers=args.markers, output_format=output_format, no_auto_groups=no_auto_groups,
                               save_whitelist=save_whitelist)
    prepare_data.execute()
    for tmp_file in tmp_files:
        os.remove(tmp_file)


if __name__ == '__main__':
    import sys

    main(sys.argv)
