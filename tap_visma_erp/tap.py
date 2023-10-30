"""VismaERP tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_visma_erp import streams


class TapVismaERP(Tap):
    """VismaERP tap class."""

    name = "tap-visma-erp"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "tenant_id",
            th.StringType,
            required=True,
            secret=True,
            description="The tenant ID of the Visma organization.",
        ),
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            secret=True,
            description="The client id",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,
            description="The client secret",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
            default="2022-10-01",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.VismaERPStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.DepartmentStream(self),
        ]


if __name__ == "__main__":
    TapVismaERP.cli()
