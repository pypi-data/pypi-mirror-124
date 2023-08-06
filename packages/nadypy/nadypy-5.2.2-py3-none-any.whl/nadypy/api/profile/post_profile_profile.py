from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...types import Response


def _get_kwargs(
    profile: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/profile/{profile}".format(client.base_url, profile=profile)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    profile: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    kwargs = _get_kwargs(
        profile=profile,
        client=client,
    )

    response = client.client.post(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    profile: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    kwargs = _get_kwargs(
        profile=profile,
        client=client,
    )

    response = await client.async_client.post(**kwargs)

    return _build_response(response=response)
