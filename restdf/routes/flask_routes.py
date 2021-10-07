# Built-in modules
import time
from datetime import datetime

# Third-party modules
import flask
import pandas as pd
from flask_cors import cross_origin
from flask import Blueprint, jsonify, request, Response

# RestDF modules
from ..utils import helper, exceptions


dataframe: pd.DataFrame = None
file_name: str = None
flask_blueprint = Blueprint('restdf', __name__)

# Runtime info variables
_runtime        : float = time.time()
_running_since  : str   = str(datetime.now())
_total_requests : int   = 0
_values_requests: int   = 0

def get_flask_blueprint(df: pd.DataFrame, fname: str) -> Blueprint:
    global dataframe
    global file_name
    if isinstance(df, pd.DataFrame):
        dataframe = df
        file_name = fname
    else:
        raise TypeError(f'DataFrame expected, found {type(df)}')
    return flask_blueprint

######################################################################
#                            ROUTES                                  #
######################################################################

@cross_origin
@flask_blueprint.route('/', methods=['GET'])
def root() -> Response:
    global _total_requests; _total_requests += 1
    return jsonify(helper.get_index(file_name))

@cross_origin
@flask_blueprint.route('/stats', methods=['GET'])
def get_stats() -> Response:
    global _total_requests; _total_requests += 1
    stats = {
        'filename'        : file_name,
        'runtime_duration': time.time() - _runtime,
        'running_since'   : _running_since,
        'total_requests'  : _total_requests,
        'values_requests' : _values_requests
    }
    return jsonify(helper.get_stats('Flask', flask.__version__, stats))

@cross_origin
@flask_blueprint.route('/columns', methods=['GET'])
def get_columns() -> Response:
    global _total_requests; _total_requests += 1
    return jsonify({'columns': helper.get_dataframe_columns(dataframe)})

@cross_origin
@flask_blueprint.route('/describe', methods=['POST'])
def get_describe() -> Response:
    global _total_requests; _total_requests += 1
    request_body = request.get_json()
    request_body = request_body if isinstance(request_body, dict) else {}
    try:
        df_description = helper.get_dataframe_descriptions(
            dataframe, **request_body
        )
    except exceptions.InvalidRequestBodyError as inv_req:
        return jsonify({'error': str(inv_req)})
    else:
        return jsonify({'description': df_description})

@cross_origin
@flask_blueprint.route('/info', methods=['GET'])
def get_info() -> Response:
    global _total_requests; _total_requests += 1
    info = helper.get_dataframe_info(dataframe)
    return jsonify({'info': info, 'shape': dataframe.shape})

@cross_origin
@flask_blueprint.route('/value_counts/<column>', methods=['GET'])
def get_value_counts(column: str):
    try:
        vc = helper.get_value_counts(dataframe, column)
    except KeyError:
        return jsonify({'error': f'Column "{column}" is not present in the dataframe. Please check /columns'})
    else:
        return jsonify({'column': column, 'value_counts': vc})

@cross_origin
@flask_blueprint.route('/nulls', methods=['GET'])
def get_info() -> Response:
    global _total_requests; _total_requests += 1
    nulls = pd.isna(dataframe).sum().to_dict()
    return jsonify(nulls)
