import pickle
from grpc.aio import Channel
from app.worker.grpc.scheduler_pb2_grpc import SchedulerWorkerStub
from app.worker.grpc.scheduler_pb2 import (
    AddTaskRequest,
    TaskIdRequest,
    RemoveResponse
)


class SchedulerService:
    def __init__(
        self,
        channel: Channel,
    ):
        self.channel = channel

    async def add_task(self, task_obj):
        task_obj_bytes = pickle.dumps(task_obj)
        async with self.channel as channel:
            worker_stub = SchedulerWorkerStub(channel)
            request = AddTaskRequest(
                task_obj=task_obj_bytes,
                timeout=1
            )
            return await worker_stub.add_task(request)

    async def remove_task(self, task_id: str):
        async with self.channel as channel:
            worker_stub = SchedulerWorkerStub(channel)
            response: RemoveResponse = await worker_stub.remove_task(
                TaskIdRequest(task_id=str(task_id))
            )
            return response.success
