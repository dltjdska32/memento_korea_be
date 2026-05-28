import logging

import httpx
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.common.config.response import Response
from app.common.exception.base_exception import BaseException


logger = logging.getLogger(__name__)



def error_response(status_code: int, code: str, message: str) -> JSONResponse:
    body = Response.error(status_code, code, message)
    return JSONResponse(status_code=status_code, content=body.model_dump())


def register_exception_handlers(app: FastAPI) -> None:

    # 1. 커스텀 예외 (BaseException)
    @app.exception_handler(BaseException)
    async def handle_base_exception(request: Request, exc: BaseException):
        logger.error("%s: %s", exc.code, exc.message)
        return error_response(exc.status_code, exc.code, exc.message)

    # 2. 외부 API 호출 예외
    @app.exception_handler(httpx.HTTPError)
    async def handle_external_api_exception(request: Request, exc: httpx.HTTPError):
        logger.error("API_ERR: %s", str(exc))
        return error_response(500, "API_ERR", "외부 API 호출 오류 발생")

    # 3. 도메인 / 잘못된 인자
    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError):
        logger.error("DOMAIN_ETC_ERR: %s", str(exc))
        return error_response(500, "DOMAIN_ETC_ERR", str(exc))

    # 5. 요청 검증 예외 (@Valid, @ModelAttribute 대응)
    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(request: Request, exc: RequestValidationError):
        messages = []
        for err in exc.errors():
            field = ".".join(str(loc) for loc in err["loc"] if loc != "body")
            messages.append(f"{field}: {err['msg']}")
        msg = ", ".join(messages)
        logger.error("INVALID_PARAM: %s", msg)
        return error_response(400, "INVALID_PARAM", msg)

    # 6. HTTPException (헤더 누락, 404 등)
    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 401:
            return error_response(401, "AUTH_ERR", "접근 권한 오류 발생")
        if exc.status_code == 400 and "header" in str(exc.detail).lower():
            logger.error("MISSING_HEADER_ERR: %s", exc.detail)
            return error_response(400, "MISSING_HEADER_ERR", "필수 헤더 누락 오류 발생.")
        return error_response(exc.status_code, "HTTP_ERR", str(exc.detail))

    # 7. 기타 서버 에러 (가장 마지막에 잡히는 것들)
    @app.exception_handler(Exception)
    async def handle_internal_server_exception(request: Request, exc: Exception):
        logger.exception("INTERNAL_SERVER_ERR")
        return error_response(500, "INTERNAL_SERVER_ERR", "서버 내부 오류 발생.")