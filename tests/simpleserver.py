"""A simple HTTP server for testing CITE runner."""

import dataclasses
import json
import logging
import functools
from typing import Protocol
from http.client import HTTPMessage
from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Collection:
    id: str
    title: str
    description: str
    keywords: str
    links: str
    extent: str
    item_type: str
    crs: str
    storage_crs: str


class DataCatalog:
    collections: dict[str, Collection]

    def __init__(self):
        self.collections = {
            "test-collection-1": Collection(
                id="test-collection-1",
                title="Test Collection 1",
                description="This is a test collection",
                keywords="test, collection, 1",
                links="https://example.com/test-collection-1",
                extent="100, 100",
                item_type="test-item-type",
                crs="EPSG:4326",
                storage_crs="EPSG:4326",
            ),
        }

    def list_collections(self) -> list[Collection]:
        return self.collections

    def get_collection(self, collection_id: str) -> Collection: ...


@functools.cache
def get_catalog():
    return DataCatalog()


class RequestHandler(Protocol):
    def __call__(
        self,
        headers: HTTPMessage,
        query: str | None = None,
        encoding: str = "utf-8",
        **path_parameters: dict[str:str],
    ) -> tuple[int, dict[str, str], bytes]: ...


class CiteRunnerApiFeaturesHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        encoding = "utf-8"
        path, query = self.path.partition("?")[::2]
        path = path.strip("/")
        logger.debug(f"{self.path=}")
        logger.debug(f"path={path!r}, query={query!r}")
        handler_info = select_handler(path)
        if handler_info is not None:
            try:
                handler, path_parameters = handler_info
            except TypeError:
                handler = handler_info
                path_parameters = {}
            status, headers, body = handler(
                self.headers, query=query, encoding=encoding, **path_parameters
            )
        else:
            status, headers, body = (
                404,
                {
                    "Content-type": f"application/json; charset={encoding}",
                },
                json.dumps({"error": "Not found"}).encode(encoding),
            )
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)


def select_handler(
    path: str,
) -> RequestHandler | RequestHandler | tuple[RequestHandler, dict[str, str]] | None:
    match path.split("/"):
        case [""]:
            return get_landing_page
        case ["collections"]:
            return list_collections
        case ["collections", collection_id]:
            return get_collection, {"collection_id": collection_id}
        case _:
            return None


def get_landing_page(
    headers: HTTPMessage, query: str | None = None, encoding: str = "utf-8"
) -> tuple[int, dict[str, str], bytes]:
    return (
        200,
        {
            "Content-type": f"application/json; charset={encoding}",
        },
        json.dumps(
            {
                "collections": [],
                "links": [
                    {
                        "type": "application/json",
                        "rel": "self",
                        "title": "This document",
                        "href": "",
                    }
                ],
            },
        ).encode(encoding),
    )


def list_collections(
    headers: HTTPMessage, query: str | None = None, encoding: str = "utf-8"
) -> tuple[int, dict[str, str], bytes]:
    catalog = get_catalog()
    serialized_collections = []
    for collection in catalog.list_collections():
        serialized_collections.append(dataclasses.asdict(collection))

    return (
        200,
        {
            "Content-type": f"application/json; charset={encoding}",
        },
        json.dumps(
            {
                "original_query_was": query,
                "collections": serialized_collections,
            },
        ).encode(encoding),
    )


def get_collection(
    headers: HTTPMessage,
    query: str | None = None,
    encoding: str = "utf-8",
    *,
    collection_id: str,
) -> tuple[int, dict[str, str], bytes]:
    return (
        200,
        {
            "Content-type": f"application/json; charset={encoding}",
        },
        json.dumps(
            {
                "collection_id_was": collection_id,
                "original_query_was": query,
            },
        ).encode(encoding),
    )


def main(bind_address: str = "localhost", port: int = 8000):
    httpd = HTTPServer((bind_address, port), CiteRunnerApiFeaturesHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
