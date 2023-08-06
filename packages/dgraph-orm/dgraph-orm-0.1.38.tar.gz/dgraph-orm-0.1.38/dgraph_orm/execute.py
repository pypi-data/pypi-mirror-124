import typing as T
import os
import time
import httpx
from httpx import Response
from . import GQLException

URL = os.environ["DGRAPH_URL"]
TIMEOUT = os.getenv("DGRAPH_TIMEOUT", 25.0)

client_sync = httpx.Client(timeout=TIMEOUT)
client = httpx.AsyncClient(timeout=TIMEOUT)


def check_for_errors(j: dict) -> None:
    if errors := j.get("errors"):
        raise GQLException(errors)


def finish(
    *, response: Response, query_str: str, should_print: bool, start_time: float
) -> dict:
    j = response.json()
    print(
        f"took: {(time.time() - start_time) * 1000}, "
        f'took internal: {int(j["extensions"]["tracing"]["duration"]) / (10 ** 6)}'
    )
    if should_print:
        print(f"{query_str=}, {j=}")
    check_for_errors(j)
    if "data" not in j:
        raise GQLException(f"data not in j!, {j=}, {query_str=}")
    return j


def gql_sync(
    query_str: str,
    variables: dict = None,
    should_print: bool = False,
    url: T.Optional[str] = None,
) -> dict:
    start = time.time()
    response = client_sync.post(
        url=url or URL, json={"query": query_str, "variables": variables or {}}
    )
    return finish(
        response=response,
        query_str=query_str,
        should_print=should_print,
        start_time=start,
    )


async def gql(
    query_str: str,
    variables: dict = None,
    should_print: bool = False,
    url: T.Optional[str] = None,
) -> dict:
    start = time.time()
    response = await client.post(
        url=url or URL, json={"query": query_str, "variables": variables or {}}
    )
    return finish(
        response=response,
        query_str=query_str,
        should_print=should_print,
        start_time=start,
    )
