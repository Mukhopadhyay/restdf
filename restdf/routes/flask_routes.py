# Built-in modules
import time
from datetime import datetime

# Third-party modules
import flask
import pandas as pd
from flask_cors import cross_origin
from flask import Blueprint, json, jsonify, request, Response

# RestDF modules
from ..utils import helper


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
def index() -> Response:
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
