from typing import AsyncGenerator
import grpc
from grpc.aio import Channel

from app.core.settings import get_settings

settings = get_settings()


async def provide_worker_channel() -> AsyncGenerator[Channel, None]:
    return grpc.aio.insecure_channel(settings.worker_socket)
