from typing import Generic, TypeVar
from pydantic import BaseModel
T = TypeVar("T")

# 응답 포맷
class Response(BaseModel, Generic[T]):


    status_code: int
    code: str
    message: str
    value: T | None = None

    # 기본 응답 벨류x
    # 스태틱 메서드
    @classmethod
    def ok(cls) -> "Response[None]":
        return cls(status_code=200, code="SUCCESS", message="OK", value=None)

    # 기본 응답 벨류o
    @classmethod
    def ok_with_value(cls, value: T) -> "Response[T]":
        return cls(status_code=200, code="SUCCESS", message="OK", value=value)

    @classmethod
    def ok_with_status(cls, status_code: int, value: T)  -> "Response[T]":
        return cls(status_code=status_code, code="SUCCESS", message="ok", value=value)

    @classmethod
    def error(cls, status_code: int, code: str, message: str) -> "Response[None]":
        return cls(status_code=status_code, code=code, message=message, value=None)