from . import models, metadata
from typing import Dict, Any, List

endpoints = [
    ('/', 'get', metadata.index_path_kwargs),
    ('/stats', 'get', metadata.stats_path_kwargs),
    ('/columns', 'get', metadata.columns_path_kwargs),
    ('/describe', 'post', metadata.describe_path_kwargs),
    ('/dtypes', 'get', metadata.dtypes_path_kwargs),
    ('/info', 'get', metadata.info_path_kwargs),
    ('/nulls', 'get', metadata.nulls_path_kwargs),
    ('/value_counts/{column_name}', 'get', metadata.value_counts_path_kwargs),
    ('/equals/{column_name}', 'post', metadata.equals_path_kwargs),
    ('/find_string/{column_name}', 'post', metadata.find_string_path_kwargs),
    ('/head', 'post', metadata.head_path_kwargs),
    ('/isin/{column_name}', 'post', metadata.isin_path_kwargs),
    ('/not_equals/{column_name}', 'post', metadata.not_equals_path_kwargs),
    ('/notin/{column_name}', 'post', metadata.notin_path_kwargs),
    ('/sample', 'post', metadata.sample_path_kwargs),
    ('/values/{column_name}', 'post', metadata.values_path_kwargs)
]


def get_column_path_param(column_names: List[str]) -> Dict[str, Any]:
    return {
        'name': 'column_name',
        'in': 'path',
        'description': "Name of the column on which we're performing the operation",
        'required': True,
        'type': 'string',
        'enum': column_names
    }


def create_paths(column_names: List[str]) -> Dict[str, Any]:
    paths: Dict[str, Any] = {}
    for (ep, method, kwargs) in endpoints:
        path_dict = models.SwaggerEndpoint(**kwargs)
        if ep.endswith(r'}'):
            path_dict.parameters.append(get_column_path_param(column_names))
        paths[ep] = {method: path_dict.__dict__}

    return paths


def get_swagger_template(column_names: List[str]) -> Dict[str, Any]:
    con = {'email': 'praneshmukherjee7@gmail.com'}
    lic = {'name': 'MIT', 'url': 'https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE'}
    template = models.SwaggerTemplate(
        info=models.InfoTemplate(contact=con, license=lic).__dict__,
        tags=[models.Tag(n, d).__dict__ for (n, d) in metadata.tags],
        schemes=['http'],
        paths=create_paths(column_names),
        definitions=metadata.definitions
    )
    return template.__dict__
