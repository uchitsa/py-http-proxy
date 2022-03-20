import requests
from flask import Flask, Response, request, current_app
import argparse


def create_app():
    app = Flask(__name__)

    @app.route("/", defaults={"uri_path": ""}, methods=["GET"])
    def default(uri_path):
        if not uri_path.startswith("/"):
            uri_path = "/" + uri_path
        else:
            uri_path = "/"

        url = "https://thehackernews.com" + uri_path
        headers = dict(request.headers.items())
        headers.pop("Host", None)

        req = requests.Session().get(url, headers=headers)
        current_app.logger.info("%s %s - %s", url, req, req.elapsed.total_seconds())
        response_headers = dict(req.headers.items())
        exclude_headers = ('Content-Encoding', 'Transfer-Encoding', 'Content-Length', 'P3P', 'Public-Key-Pins',
                           'Connection', 'Keep-Alive')

        return Response()

    return app


if __name__ == "main":
    prsr = argparse.ArgumentParser()
    prsr.add_argument("--host", default="0.0.0.0", type=str)
    prsr.add_argument("--port", default="8088", type=int)
    prsr.add_argument("--debug", action="store_true")

    args = prsr.parse_args()
    app = create_app()
    app.run(host=args.host, port=args.port, debug=args.port)
