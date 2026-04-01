"""Clerk as OAuth/OIDC upstream for FastMCP (Clerk as identity provider).

See https://clerk.com/docs/advanced-usage/clerk-idp for dashboard setup:
OAuth application, Discovery URL, Client ID / Secret, redirect URIs.
"""

from __future__ import annotations

from typing import Literal

from key_value.aio.protocols import AsyncKeyValue
from pydantic import AnyHttpUrl

from fastmcp.server.auth.oidc_proxy import OIDCProxy
from fastmcp.utilities.auth import parse_scopes
from fastmcp.utilities.logging import get_logger

logger = get_logger(__name__)


class ClerkAuthProvider(OIDCProxy):
    """FastMCP auth using Clerk as the upstream OIDC provider.

    Pass ``config_url`` from the Clerk OAuth application's Discovery URL.
    Default scopes are ``profile`` and ``email`` only, matching Clerk OAuth apps
    that do not enable ``openid``. Enable ``openid`` on the OAuth application in
    the Clerk Dashboard (and pass ``required_scopes`` including ``openid``) for
    full OIDC / ``id_token`` flows.

    If Clerk issues opaque access tokens, set ``verify_id_token=True`` so the
    validated JWT is the OIDC ``id_token`` (audience = OAuth client_id); that
    requires the ``openid`` scope on the Clerk app.
    """

    def __init__(
        self,
        *,
        config_url: AnyHttpUrl | str,
        client_id: str,
        client_secret: str,
        audience: str | None = None,
        base_url: AnyHttpUrl | str,
        issuer_url: AnyHttpUrl | str | None = None,
        required_scopes: list[str] | None = None,
        redirect_path: str | None = None,
        allowed_client_redirect_uris: list[str] | None = None,
        client_storage: AsyncKeyValue | None = None,
        jwt_signing_key: str | bytes | None = None,
        verify_id_token: bool = False,
        require_authorization_consent: bool | Literal["external"] = True,
        consent_csp_policy: str | None = None,
    ) -> None:
        clerk_scopes = (
            parse_scopes(required_scopes)
            if required_scopes is not None
            else ["profile", "email"]
        )

        super().__init__(
            config_url=config_url,
            client_id=client_id,
            client_secret=client_secret,
            audience=audience,
            base_url=base_url,
            issuer_url=issuer_url,
            redirect_path=redirect_path,
            required_scopes=clerk_scopes,
            allowed_client_redirect_uris=allowed_client_redirect_uris,
            client_storage=client_storage,
            jwt_signing_key=jwt_signing_key,
            verify_id_token=verify_id_token,
            require_authorization_consent=require_authorization_consent,
            consent_csp_policy=consent_csp_policy,
        )

        logger.debug(
            "Initialized Clerk OIDC proxy for client %s with scopes: %s",
            client_id,
            clerk_scopes,
        )
