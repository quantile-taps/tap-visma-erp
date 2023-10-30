"""Stream type classes for tap-visma-erp."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_visma_erp.client import VismaERPStream


class DepartmentStream(VismaERPStream):
    """Define custom stream."""

    name = "department"
    path = "/department"
    primary_keys = ["departmentId"]

    schema = th.PropertiesList(
        th.Property("departmentId", th.StringType),
        th.Property("publicId", th.StringType),
        th.Property("description", th.StringType),
        th.Property("expenseSubaccount", th.ObjectType(
            th.Property("id", th.StringType)
        )),
        th.Property("lastModifiedDateTime", th.DateTimeType),
    ).to_dict()


