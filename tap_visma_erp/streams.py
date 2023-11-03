"""Stream type classes for tap-visma-erp."""

from __future__ import annotations
import datetime
from singer_sdk import typing as th  # JSON Schema typing helpers

from typing import Any

from tap_visma_erp.client import VismaERPStream


class DepartmentStream(VismaERPStream):
    """Fetch departments from Visma."""

    name = "department"
    path = "/controller/api/v1/department"
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

class AccountStream(VismaERPStream):
    """Fetch accounts from Visma."""

    name = "account"
    path = "/controller/api/v1/account"
    primary_keys = ["accountID"]

    schema = th.PropertiesList(
        th.Property("accountID", th.IntegerType),
        th.Property("accountCD", th.StringType),
        th.Property("accountClass", th.StringType),
        th.Property("type", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("description", th.StringType),
        th.Property("useDefaultSub", th.BooleanType),
        th.Property("postOption", th.StringType),
        th.Property("cashAccount", th.BooleanType),
        th.Property("lastModifiedDateTime", th.DateTimeType),
    ).to_dict()

class LedgerStream(VismaERPStream):
    """Fetch ledgers from Visma."""

    name = "ledger"
    path = "/controller/api/v1/ledger"
    primary_keys = ["internalId"]

    schema = th.PropertiesList(
        th.Property("internalId", th.IntegerType),
        th.Property("number", th.StringType),
        th.Property("description", th.StringType),
        th.Property("balanceType", th.StringType),
        th.Property("currencyId", th.StringType),
        th.Property("consolidationSource", th.BooleanType),
        th.Property("branchAccounting", th.BooleanType),
        th.Property("lastModifiedDateTime", th.DateTimeType),
        th.Property("postInterCompany", th.BooleanType),
    ).to_dict()

class SubAccountStream(VismaERPStream):
    """Fetch sub accounts from Visma."""

    name = "subaccount"
    path = "/controller/api/v1/subaccount"
    primary_keys = ["subaccountId"]

    schema = th.PropertiesList(
        th.Property("subaccountNumber", th.StringType),
        th.Property("subaccountId", th.IntegerType),
        th.Property("description", th.StringType),
        th.Property("lastModifiedDateTime", th.DateTimeType),
        th.Property("active", th.BooleanType),
        th.Property("segments", th.ArrayType(
            th.ObjectType(
                th.Property("segmentId", th.IntegerType),
                th.Property("segmentDescription", th.StringType),
                th.Property("segmentValue", th.StringType),
                th.Property("segmentValueDescription", th.StringType),
            )
        )),
    ).to_dict()

class BudgetStream(VismaERPStream):
    """Fetch budgets from Visma."""

    name = "budget"
    path = "/controller/api/v1/budget"
    primary_keys = ["financialYear"]

    partitions = [
        {"financialYear": year} 
            for year in range(2020, datetime.datetime.now().year + 1)
        ]

    schema = th.PropertiesList(
        th.Property("financialYear", th.StringType),
        th.Property("released", th.BooleanType),
        th.Property("releasedAmount", th.NumberType),
        th.Property("account", th.ObjectType(
            th.Property("type", th.StringType),
            th.Property("number", th.StringType),
            th.Property("description", th.StringType),
        )),
        th.Property("subaccount", th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("description", th.StringType),
        )),
        th.Property("description", th.StringType),
        th.Property("amount", th.NumberType),
        th.Property("distributedAmount", th.NumberType),
        th.Property("periods", th.ArrayType(
            th.ObjectType(
                th.Property("periodId", th.StringType),
                th.Property("amount", th.NumberType),
            )
        )),
        th.Property("lastModifiedDateTime", th.DateTimeType),
        th.Property("branchNumber", th.ObjectType(
            th.Property("number", th.StringType),
            th.Property("name", th.StringType),
        )),
    ).to_dict()

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
            "branch": "1",
            "ledger": "BUDGET",
            **context
        }

        return params

class GeneralLedgerBalanceStream(VismaERPStream):
    """Fetch general ledger balances from Visma."""

    name = "general_ledger_balance"
    path = "/controller/api/v2/generalLedgerBalance"
    replication_key = "lastModifiedDateTime"
    primary_keys = ["balanceType", "financialPeriod", "subaccountId"]

    schema = th.PropertiesList(
        th.Property("ledger", th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("description", th.StringType),
        )),
        th.Property("balanceType", th.StringType),
        th.Property("financialPeriod", th.StringType),
        th.Property("account", th.ObjectType(
            th.Property("type", th.StringType),
            th.Property("number", th.StringType),
            th.Property("description", th.StringType),
        )),
        th.Property("subaccountId", th.StringType),
        th.Property("subAccountCd", th.StringType),
        th.Property("currencyId", th.StringType),
        th.Property("periodToDateDebit", th.NumberType),
        th.Property("periodToDateCredit", th.NumberType),
        th.Property("beginningBalance", th.NumberType),
        th.Property("yearToDateBalance", th.NumberType),
        th.Property("periodToDateDebitInCurrency", th.NumberType),
        th.Property("periodToDateCreditInCurrency", th.NumberType),
        th.Property("beginningBalanceInCurrency", th.NumberType),
        th.Property("yearToDateBalanceInCurrency", th.NumberType),
        th.Property("yearClosed", th.StringType),
        th.Property("lastModifiedDateTime", th.DateTimeType),
    ).to_dict()
