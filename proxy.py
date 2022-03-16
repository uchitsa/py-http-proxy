import requests
import Flask
import argparse


def create_app():
    app = Flask(__name__)
    requests.Session

    @app.route("/", defaults={"uri_path": ""}, methods=["GET"])
    def default(uri_path):
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
