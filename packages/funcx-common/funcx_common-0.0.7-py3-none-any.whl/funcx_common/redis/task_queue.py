import queue
import typing as t

from ..tasks import TaskProtocol, TaskState
from .connection import _OPT_CONNECTION_FACTORY_T, HasRedisConnection


class FuncxEndpointTaskQueue(HasRedisConnection):
    def __init__(
        self,
        hostname: str,
        endpoint: str,
        *,
        port: int = 6379,
        redis_connection_factory: _OPT_CONNECTION_FACTORY_T = None,
    ):
        self.endpoint = endpoint
        super().__init__(
            hostname, port=port, redis_connection_factory=redis_connection_factory
        )

    def _repr_attrs(self) -> t.List[str]:
        return [f"endpoint={self.endpoint}"] + super()._repr_attrs()

    @property
    def queue_name(self) -> str:
        return f"task_{self.endpoint}_list"

    def enqueue(self, task: TaskProtocol) -> None:
        task.endpoint = self.endpoint
        task.status = TaskState.WAITING_FOR_EP
        self.redis_client.rpush(self.queue_name, task.task_id)

    def dequeue(self, *, timeout: int = 1) -> str:
        res = self.redis_client.blpop(self.queue_name, timeout=timeout)
        if not res:
            raise queue.Empty
        _queue_name, task_id = res
        return t.cast(str, task_id)
