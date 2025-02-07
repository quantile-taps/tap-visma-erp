"""VismaERP Authentication."""

from __future__ import annotations

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class VismaERPAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for VismaERP."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the AutomaticTestTap API.

        Returns:
            A dict with the request body
        """
        return {
            "scope": self.oauth_scopes,
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "tenant_id": self.config["tenant_id"],
            "grant_type": "client_credentials",
        }

    @classmethod
    def create_for_stream(cls, stream) -> VismaERPAuthenticator:  # noqa: ANN001
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        return cls(
            stream=stream,
            auth_endpoint="https://connect.visma.com/connect/token",
            oauth_scopes="vismanet_erp_service_api:read",
        )
