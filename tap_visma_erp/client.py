"""REST client handling, including VismaERPStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable

import requests
from requests import Response
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import (
    BaseAPIPaginator,
    BasePageNumberPaginator,
)  # noqa: TCH002
from singer_sdk.streams import RESTStream

from tap_visma_erp.auth import VismaERPAuthenticator

from functools import cached_property
import pendulum

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class SimplePaginator(BasePageNumberPaginator):
    """Custom paginator"""

    def has_more(self, response: Response) -> bool:
        """If records have a `metadata` key pagination is possible. We keep fetching until no records returned.

        Args:
            response: API response object.

        Returns:
            Boolean flag used to indicate if the endpoint has more pages.
        """
        data = response.json()

        if len(data) > 0 and "metadata" in data[-1]:
            return True
        else:
            return False


class VismaERPStream(RESTStream):
    """VismaERP stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root"""
        return "https://integration.visma.net/API"

    records_jsonpath = "$[*]"  # Or override `parse_response`.

    # Set this value or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @cached_property
    def authenticator(self) -> _Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return VismaERPAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_new_paginator(self) -> BaseAPIPaginator:
        return SimplePaginator(start_value=1)

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {
            "pageSize": 1000,
        }
        if next_page_token:
            params["pageNumber"] = next_page_token

        if self.replication_key:

            starting_timestamp = self.get_starting_timestamp(context)
            params["lastModifiedDateTime"] = pendulum.instance(
                starting_timestamp
            ).to_datetime_string()

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())
