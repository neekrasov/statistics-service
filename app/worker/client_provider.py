from typing import AsyncGenerator
import grpc
from grpc.aio import Channel


async def provide_worker_channel() -> AsyncGenerator[Channel, None]:
    return grpc.aio.insecure_channel("localhost:50051")
