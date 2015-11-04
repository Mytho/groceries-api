#!/usr/bin/env python
import argparse
import os
import sys

sys.path.append(os.path.abspath('.'))

from application.core import make_app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='the hostname to listen on',
                        default='127.0.0.1')
    parser.add_argument('-p', '--port', help='the port of the webserver',
                        type=int, default=5000)
    parser.add_argument('-d', '--debug', help='if given, enable debug mode',
                        action='store_true', default=False)
    args = parser.parse_args()
    app = make_app()
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
