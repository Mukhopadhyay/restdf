# Built-in modules
import os

# Third-party modules
from flask import Flask
from flask_cors import CORS

# RestDF Modules
from .configs import settings
from .utils import (io, utils)
from .routes import flask_routes

app = Flask(__name__)


# Main method
def main() -> None:
    args = utils.get_parser().parse_args()

    df_path = args.path
    # log_path = args.path          # TBI
    flask_kwargs = {
        'host':  settings.HOST if not args.host else args.host,
        'port':  settings.PORT if not args.port else args.port,
        'debug': settings.DEBUG if not args.debug else args.debug
    }

    # Reading the dataframe
    dataframe = io.read_dataframe(df_path)

    app = flask_routes.get_flask_app(
       df=dataframe,
       fname=os.path.split(df_path)[-1]
    )

    # Start the API
    CORS(app=app)
    app.run(**flask_kwargs)


# Nohup run: nohup python3 -m restdf /absolute/path/to/df > stdlog.txt 2>&1 &
if __name__ == '__main__':
    main()
