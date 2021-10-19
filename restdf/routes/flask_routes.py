# Built-in modules
import time
from datetime import datetime
from typing import Optional, Tuple
# Third-party modules
import flask
import pandas as pd
from flask_cors import cross_origin
from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request, Response
# RestDF modules
from ..configs import config
from ..utils import helper, exceptions

dataframe: Optional[pd.DataFrame] = None
file_name: str = ''
app: Flask = Flask(__name__)

# Runtime info variables
_runtime: float = time.time()
_running_since: str = str(datetime.now())
_total_requests: int = 0
_values_requests: int = 0


def get_flask_app(df: pd.DataFrame, filename: str, api_title: Optional[str] = None) -> Flask:
    global dataframe
    global file_name

    if isinstance(df, pd.DataFrame):
        dataframe = df
        file_name = filename
    else:
        raise TypeError(f'DataFrame expected, found {type(df)}')

    # Setting up SwaggerUI
    # Swagger template
    flasgger_template = config.flasgger_template
    flasgger_template['info']['title'] = f'{file_name} API'

    # Swagger config
    flasgger_config = config.flasgger_config
    app.config['SWAGGER'] = {
        'title': api_title if api_title else f'{file_name} API',
        'uiversion': 3
    }
    Swagger(app, template=flasgger_template, config=flasgger_config)

    return app

######################################################################
#                            ROUTES                                  #
######################################################################


@cross_origin
@app.route('/', methods=['GET'])
@swag_from('flask_schemas/index.yml')
def root() -> Response:
    global _total_requests
    _total_requests += 1
    return jsonify(helper.get_index(file_name))


@cross_origin
@app.route('/stats', methods=['GET'])
@swag_from('flask_schemas/stats.yml')
def get_stats() -> Response:
    global _total_requests
    _total_requests += 1
    stats = {
        'filename': file_name,
        'runtime_duration': time.time() - _runtime,
        'running_since': _running_since,
        'total_requests': _total_requests,
        'values_requests': _values_requests
    }
    return jsonify(helper.get_stats('Flask', flask.__version__, stats))


@cross_origin
@swag_from('flask_schemas/columns.yml')
@app.route('/columns', methods=['GET'])
def get_columns() -> Response:
    global _total_requests
    _total_requests += 1
    return jsonify({'columns': helper.get_dataframe_columns(dataframe)})


@cross_origin
@swag_from('flask_schemas/describe.yml')
@app.route('/describe', methods=['POST'])
def get_describe() -> Tuple[Response, int]:
    global _total_requests
    _total_requests += 1
    request_body = request.get_json()
    request_body = request_body if isinstance(request_body, dict) else {}
    try:
        df_description = helper.get_dataframe_descriptions(
            dataframe, **request_body
        )
    except exceptions.InvalidRequestBodyError as inv_req:
        return jsonify({'error': str(inv_req)}), 500
    else:
        return jsonify({'description': df_description}), 200


@cross_origin
@swag_from('flask_schemas/info.yml')
@app.route('/info', methods=['GET'])
def get_info() -> Response:
    global _total_requests
    _total_requests += 1

    info = helper.get_dataframe_info(dataframe)
    return jsonify({'info': info, 'shape': dataframe.shape})


@cross_origin
@swag_from('flask_schemas/dtypes.yml')
@app.route('/dtypes', methods=['GET'])
def get_dtypes() -> Response:
    global _total_requests
    _total_requests += 1

    return jsonify(
        {'dtypes': {k: str(v) for (k, v) in dataframe.dtypes.to_dict().items()}}
    )


@cross_origin
@swag_from('flask_schemas/value_counts.yml')
@app.route('/value_counts/<column_name>', methods=['GET'])
def get_value_counts(column_name: str) -> Tuple[Response, int]:
    global _total_requests
    _total_requests += 1

    try:
        vc = helper.get_value_counts(dataframe, column_name)
    except KeyError:
        return jsonify({'error': f'Column "{column_name}" is not present in the dataframe. Please check /columns'}), 500
    else:
        return jsonify({'column': column_name, 'value_counts': vc}), 200


@cross_origin
@swag_from('flask_schemas/nulls.yml')
@app.route('/nulls', methods=['GET'])
def get_nulls() -> Tuple[Response, int]:
    global _total_requests
    _total_requests += 1

    nulls = pd.isna(dataframe).sum().to_dict()
    return jsonify({"nulls": nulls}), 200


@cross_origin
@swag_from('flask_schemas/head.yml')
@app.route('/head', methods=['POST'])
def get_df_head() -> Tuple[Response, int]:
    global _total_requests
    _total_requests += 1

    request_body = request.get_json()
    request_body = request_body if isinstance(request_body, dict) else {}

    try:
        df_head_data = helper.get_dataframe_head(dataframe, request_body)
    except KeyError as key_error:
        return jsonify({'error': f'KeyError: {str(key_error)}'}), 500
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    else:
        return jsonify({'head': df_head_data}), 200


@cross_origin
@swag_from('flask_schemas/sample.yml')
@app.route('/sample', methods=['POST'])
def get_df_sample() -> Response:
    global _total_requests
    _total_requests += 1

    request_body = request.get_json()

    request_body = request_body if isinstance(request_body, dict) else {}
    df_sample_data = helper.get_dataframe_sample(
        dataframe, request_body
    )

    return jsonify({'sample': df_sample_data})


@cross_origin
@swag_from('flask_schemas/values.yml')
@app.route('/values/<column_name>', methods=['POST'])
def get_column_value(column_name: str) -> Response:
    global _total_requests
    global _values_requests
    _total_requests += 1
    _values_requests += 1

    request_body = request.get_json()
    request_body = request_body if isinstance(request_body, dict) else {}
    try:
        values = helper.get_column_value(
            dataframe, column_name, request_body
        )
    except KeyError:
        return jsonify({'error': f'Column "{column_name}" is not present in the dataframe. Please check /columns'})
    else:
        return jsonify({'values': values})


@cross_origin
@swag_from('flask_schemas/isin.yml')
@app.route('/isin/<column_name>', methods=['POST'])
def get_isin_values(column_name: str) -> Response:
    global _total_requests
    global _values_requests
    _total_requests += 1
    _values_requests += 1

    request_body = request.get_json()
    request_body = request_body if isinstance(request_body, dict) else {}
    try:
        values = helper.get_isin_values(
            dataframe, column_name, request_body
        )
    except KeyError:
        return jsonify({'error': f'Column "{column_name}" is not present in the dataframe. Please check /columns'})
    else:
        return jsonify({'values': values})


@cross_origin
@swag_from('flask_schemas/notin.yml')
@app.route('/notin/<column_name>', methods=['POST'])
def get_notin_values(column_name: str) -> Response:
    global _total_requests
    global _values_requests
    _total_requests += 1
    _values_requests += 1

    request_body = request.get_json()
    request_body = request_body if isinstance(request_body, dict) else {}
    try:
        values = helper.get_notin_values(
            dataframe, column_name, request_body
        )
    except KeyError:
        return jsonify({'error': f'Column "{column_name}" is not present in the dataframe. Please check /columns'})
    else:
        return jsonify(values)


@cross_origin
@swag_from('flask_schemas/equals.yml')
@app.route('/equals/<column_name>', methods=['POST'])
def get_equal_values(column_name: str) -> Response:
    global _total_requests
    global _values_requests
    _total_requests += 1
    _values_requests += 1

    request_body = request.get_json()
    request_body = request_body if isinstance(request_body, dict) else {}

    try:
        values = helper.get_equal_values(dataframe,
                                         column_name,
                                         request_body)
    except KeyError:
        return jsonify({'error': f'Column "{column_name}" is not present in the dataframe. Please check /columns'})
    else:
        return jsonify(values)


@cross_origin
@swag_from('flask_schemas/not_equals.yml')
@app.route('/not_equals/<column_name>', methods=['POST'])
def get_not_equal_values(column_name: str) -> Response:
    global _total_requests
    global _values_requests
    _total_requests += 1
    _values_requests += 1

    request_body = request.get_json()
    request_body = request_body if isinstance(request_body, dict) else {}

    try:
        values = helper.get_not_equal_values(
            dataframe, column_name, request_body
        )
    except KeyError:
        return jsonify({'error': f'Column "{column_name}" is not present in the dataframe. Please check /columns'})
    else:
        return jsonify(values)


@cross_origin
@swag_from('flask_schemas/find_string.yml')
@app.route('/find_string/<column_name>', methods=['POST'])
def get_find_string_values(column_name: str) -> Response:
    global _total_requests
    global _values_requests
    _total_requests += 1
    _values_requests += 1

    request_body = request.get_json()

    request_body = request_body if isinstance(request_body, dict) else {}

    try:
        used_kwargs, values, num_rec_found = helper.get_find_string_values(
            dataframe, column_name, request_body
        )
    except KeyError:
        return jsonify({'error': f'Column "{column_name}" is not present in the dataframe. Please check /columns'})
    else:
        return jsonify({
            'values': values,
            'option_used': used_kwargs,
            'num': num_rec_found
        })
