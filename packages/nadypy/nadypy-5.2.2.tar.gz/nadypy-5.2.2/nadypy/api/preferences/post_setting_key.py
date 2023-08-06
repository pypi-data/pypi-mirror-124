from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...types import Response


def _get_kwargs(
    key: str,
    *,
    client: AuthenticatedClient,
    json_body: str,
) -> Dict[str, Any]:
    url = "{}/setting/{key}".format(client.base_url, key=key)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body

    return {
        "url": url,
        "headers": headers,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    json_body: str,
) -> Response[Any]:
    kwargs = _get_kwargs(
        key=key,
        client=client,
        json_body=json_body,
    )

    response = client.client.post(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    json_body: str,
) -> Response[Any]:
    kwargs = _get_kwargs(
        key=key,
        client=client,
        json_body=json_body,
    )

    response = await client.async_client.post(**kwargs)

    return _build_response(response=response)
