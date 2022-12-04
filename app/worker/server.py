import asyncio
import pickle
import grpc
import logging

from .grpc import (
    scheduler_pb2 as scheduler_worker_messages,
    scheduler_pb2_grpc as scheduler_worker_service
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import sessionmaker

from app.core.settings import get_settings
from app.db.base import create_session_factory
from app.schemas.task import Task
from .services.scheduler import add_task_to_scheduler, start_tasks
from .services.logger import init_logger


class SchedulerWorkerService(scheduler_worker_service.SchedulerWorkerServicer):
    def __init__(
        self,
        scheduler: AsyncIOScheduler,
        sessionmaker: sessionmaker,
    ):
        self.scheduler = scheduler
        self.sessionmaker = sessionmaker

    async def add_task(
        self,
        request: scheduler_worker_messages.AddTaskRequest,
        context: grpc.aio.ServicerContext,
    ) -> scheduler_worker_messages.ResponseStub:
        task_obj: Task = pickle.loads(request.task_obj)
        async with self.sessionmaker() as session:
            logger.info(f'add_task -> {task_obj.search_phrase}')
            await add_task_to_scheduler(
                task_obj=task_obj,
                session=session,
                scheduler=self.scheduler,
                timeout=request.timeout,
            )
        return scheduler_worker_messages.ResponseStub()

    async def remove_task(
        self,
        request: scheduler_worker_messages.TaskIdRequest,
        context: grpc.aio.ServicerContext,
    ) -> scheduler_worker_messages.RemoveResponse:
        logger.info(f'remove_task -> {request.task_id}')
        self.scheduler.remove_job(str(request.task_id))

        return scheduler_worker_messages.RemoveResponse(success=True)


async def serve_worker() -> None:

    # create basics for worker
    settings = get_settings()
    scheduler = AsyncIOScheduler()
    contextsession = create_session_factory(settings.postgres_uri)

    # setup server
    server = grpc.aio.server()
    scheduler_worker_service.add_SchedulerWorkerServicer_to_server(
        server=server,
        servicer=SchedulerWorkerService(
            scheduler=scheduler,
            sessionmaker=contextsession,
        ),
    )

    server.add_insecure_port(settings.worker_socket)
    logger.info("Starting server on %s", settings.worker_socket)
    await server.start()

    logger.info("Starting tasks from db")
    await start_tasks(contextsession, scheduler, settings.parse_timeout)

    logger.info("Starting scheduler")
    scheduler.start()

    await server.wait_for_termination()


if __name__ == "__main__":
    # simple logger
    file_name = __file__.split("/")[-1]
    init_logger(file_name, logging.DEBUG)
    logger = logging.getLogger(file_name)

    # run worker
    asyncio.run(serve_worker())
