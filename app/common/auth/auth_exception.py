from app.common.exception.base_exception import BaseException

class AuthException(BaseException):
    @classmethod
    def unauthorized(cls, message: str = "로그인 후에 이용해주세요."):
        return cls(401, "JWT_AUTH_ERR", message)
    @classmethod
    def access_denied(cls, message: str = "요청한 항목에 대한 권한이 없습니다."):
        return cls(403, "JWT_INVALID_ERR", message)