import logging


from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.common.auth.auth_settings import auth_settings
from app.common.auth.auth_user_info import AuthUserInfo
from app.common.config.global_const import AUTHORIZATION_HEADER, AUTHORIZATION_HEADER_TYPE
from app.common.exception.exception_handler import error_response
from app.common.jwt.jwt_exception import JwtException
from app.common.jwt.jwt_provider import JwtProvider

logger = logging.getLogger(__name__)



class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self,
                 app,
                 jwt_provider: JwtProvider,
                 whitelist: list[str]):
        super().__init__(app)
        self.jwt_provider = jwt_provider



    async def dispatch(self,
                       req: Request,
                       call_next):

        path = req.url.path


        # CORS 요청 서버에 확인을 위한 요청은 해당 필터안탐.
        if req.method == "OPTIONS":
            return await call_next(req)

        if auth_settings.is_whitelisted(path):
            return await call_next(req)


        auth_header = req.headers.get(AUTHORIZATION_HEADER)

        if not auth_header or not auth_header.startswith(AUTHORIZATION_HEADER_TYPE):
            logger.error("인증 헤더 확인불가")
            return error_response(401, "JWT_AUTH_ERR", "로그인 후에 이용해주세요")

        #Bearer 제거
        token = auth_header.removeprefix(AUTHORIZATION_HEADER_TYPE).strip()

        if not token:
            logger.error("토큰 확인 불가")
            return error_response(401, "JWT_AUTH_ERR", "로그인 후에 이용해주세요")


        try:
            jwt_user = self.jwt_provider.get_jwt_user_info(token)
            req.state.current_user = AuthUserInfo.from_jwt(jwt_user)
        except JwtException as e:
            logger.error(e.message)
            return error_response(e.status_code, e.code, e.message)
        except Exception as e:
            logger.exception("%s", e)
            return error_response(500, "INTERNAL_SERVER_ERR", "서버 내부 오류 발생.")

        return await call_next(req)