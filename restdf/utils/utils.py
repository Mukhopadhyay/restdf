import argparse


def get_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog='RestDF',
        description='Simple API interface from a dataframe!'
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
