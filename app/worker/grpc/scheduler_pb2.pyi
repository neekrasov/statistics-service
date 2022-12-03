from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AddTaskRequest(_message.Message):
    __slots__ = ["task_obj", "timeout"]
    TASK_OBJ_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    task_obj: bytes
    timeout: int
    def __init__(self, task_obj: _Optional[bytes] = ..., timeout: _Optional[int] = ...) -> None: ...

class RemoveResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class ResponseStub(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TaskIdRequest(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...
