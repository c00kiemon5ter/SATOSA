import argparse
import functools
import os
import sys

from werkzeug.debug import DebuggedApplication
from werkzeug.serving import run_simple

import satosa.config
import satosa.proxy_server


configuration = satosa.config.parse()
app = satosa.proxy_server.make_app(configuration)


def main():
    global app

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('port', type=int)
    parser.add_argument('--keyfile', type=str)
    parser.add_argument('--certfile', type=str)
    parser.add_argument('--host', type=str)
    parser.add_argument('-d', action='store_true', dest="debug",
                        help="enable debug mode.")
    args = parser.parse_args()

    if (args.keyfile and not args.certfile) or (args.certfile and not args.keyfile):
        print("Both keyfile and certfile must be specified for HTTPS.")
        sys.exit()

    if args.debug:
        app.app = functools.partial(app.app, debug=True)
        app = DebuggedApplication(app)

    if (args.keyfile and args.certfile):
        ssl_context = (args.certfile, args.keyfile)
    else:
        ssl_context = None

    if args.host:
        run_simple(args.host, args.port, app, ssl_context=ssl_context)
    else:
        run_simple('localhost', args.port, app, ssl_context=ssl_context)


if __name__ == '__main__':
    main()
