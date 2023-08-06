from typing import Any
from typing import Dict

from dict_tools import data


async def post_gather(hub, ctx) -> Dict[str, Any]:
    return data.NamespaceDict(ctx.ret)


async def post_ctx(hub, ctx):
    return data.NamespaceDict(ctx.ret)
