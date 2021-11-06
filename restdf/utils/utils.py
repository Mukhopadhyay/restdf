import argparse


def get_parser() -> argparse.ArgumentParser:
    """
    This method returns the argument parser for the RestDF __main__ module.
    The namespace contains the following options:
        * path:     path to the dataset
        * host:     the hostname to listen on. Defaults to 'localhost'
        * port:     the port of the webserver. Defaults to 8000
        * debug:    settings this flag, makes the server run on `debug` mode.
        * title:    title of the API.
        * email:    Developer email for the SwaggerUI.

    Args:
        [None]
    Returns:
        ArgumentParser:     The argument parser with the namespace configured, ready to be parsed.
    """

    parser = argparse.ArgumentParser(
        prog='RestDF',
        description='Create a simple API from a dataframe!'
    )

    # Positional arguments
    # ---------------------
    # PATH to the dataframe
    parser.add_argument('path', metavar='PATH', action='store', type=str)

    # Optional arguments
    # HOST to run the server on
    parser.add_argument('-H', '--host', metavar='HOST', action='store', type=str)
    # PORT number to run the API on
    parser.add_argument('-p', '--port', metavar='PORT', action='store', type=int)
    # DEBUG option for the server
    parser.add_argument('-d', '--debug', action='store_true')
    # API title
    parser.add_argument('-t', '--title', metavar='TITLE', action='store', type=str)
    # User email
    parser.add_argument('-e', '--email', metavar='EMAIL', action='store', type=str)

    return parser
