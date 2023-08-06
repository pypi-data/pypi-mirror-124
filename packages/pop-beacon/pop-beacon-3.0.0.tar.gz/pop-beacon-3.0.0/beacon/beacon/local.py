import asyncio
from typing import AsyncGenerator


def __init__(hub):
    hub.beacon.local.QUEUE = None
    hub.beacon.local.STOP_ITERATION = object()


async def queue(hub):
    if hub.beacon.local.QUEUE is None:
        hub.beacon.local.QUEUE = asyncio.Queue()
    return hub.beacon.local.QUEUE


async def listen(hub) -> AsyncGenerator:
    """
    listen for data on the local queue
    """
    async for event in hub.beacon.local.channel():
        yield event


async def channel(hub) -> AsyncGenerator:
    await hub.beacon.local.queue()

    while hub.beacon.RUN_FOREVER:
        event = await hub.beacon.local.QUEUE.get()
        if event is hub.beacon.local.STOP_ITERATION:
            return
        yield event

    hub.log.debug("No more messages in local queue")


async def stop(hub):
    if hub.beacon.local.QUEUE is None:
        return
    await hub.beacon.local.QUEUE.put(hub.beacon.local.STOP_ITERATION)
