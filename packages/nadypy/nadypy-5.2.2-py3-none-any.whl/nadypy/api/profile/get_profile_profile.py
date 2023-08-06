from typing import Any, Dict, Optional, Union

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, str]]:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, str]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    profile: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, str]]:
    kwargs = _get_kwargs(
        profile=profile,
        client=client,
    )

    response = client.client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    profile: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, str]]:
    """View a profile"""

    return sync_detailed(
        profile=profile,
        client=client,
    ).parsed


async def asyncio_detailed(
    profile: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, str]]:
    kwargs = _get_kwargs(
        profile=profile,
        client=client,
    )

    response = await client.async_client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    profile: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, str]]:
    """View a profile"""

    return (
        await asyncio_detailed(
            profile=profile,
            client=client,
        )
    ).parsed
