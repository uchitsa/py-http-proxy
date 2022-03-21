import requests
from flask import Flask, Response, request, current_app
import argparse
import re
from bs4 import BeautifulSoup as bs
from bs4 import Comment

HACKERNEWS_URL = "https://thehackernews.com"


def create_app():
    app = Flask(__name__)

    @app.route("/", defaults={"uri_path": ""}, methods=["GET"])
    def default(uri_path):
        if not uri_path.startswith("/"):
            uri_path = "/" + uri_path
        else:
            uri_path = "/"

        url = HACKERNEWS_URL + uri_path
        headers = dict(request.headers.items())
        headers.pop("Host", None)

        req = requests.Session().get(url, headers=headers)
        current_app.logger.info("%s %s - %s", url, req, req.elapsed.total_seconds())
        response_headers = dict(req.headers.items())
        exclude_headers = ("Content-Encoding", "Transfer-Encoding", "Content-Length", "P3P", "Public-Key-Pins",
                           "Connection", "Keep-Alive")

        [response_headers.pop(header) for header in exclude_headers]
        content = req.content

        if req.headers.get("Content-Type", " ").startswith("text/html"):
            content = html_filter(content, request.host_url.strip("/"))

        return Response(content, content_type=req.headers["Content-Type"], headers=response_headers)

    return app


def html_filter(content, app_url):
    def filter_text(text):
        return re.sub(r"\b(?<!&amp;)(?<!&)([а-яёa-z-]{6})\b", r"\1™", text, flags=re.IGNORECASE)

    soup = bs(content, "html5lib")
    exclude_tags = ["script", "style", "noscript", "meta", "link", "code"]

    for a in soup.findAll("a", href=True):
        a["href"] = a["href"].replace(HACKERNEWS_URL, app_url) \
            .replace(HACKERNEWS_URL, app_url)

    for element in soup.find_all(text=True):
        if isinstance(element, Comment):
            continue
        text = element.string
        if text and False not in [element.find_parent(x) is None for x in exclude_tags] and text != "html":
            element.replace_with(filter_text(text))

    return soup.prettify()


if __name__ == "__main__":
    prsr = argparse.ArgumentParser()
    prsr.add_argument("--host", default="0.0.0.0", type=str)
    prsr.add_argument("--port", default="8088", type=int)
    prsr.add_argument("--debug", action="store_true")

    args = prsr.parse_args()
    app = create_app()
    app.run(host=args.host, port=args.port, debug=args.port)
