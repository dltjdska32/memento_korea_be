from app.common.exception.base_exception import BaseException

class JwtException(BaseException):

    @classmethod
    def jwt_invalid_malformed(cls, message: str = "잘못된 JWT 서명입니다."):
        return cls(401, "JWT_INVALID_MALFORMED", message)

    @classmethod
    def jwt_expired(cls, message: str = "만료된 JWT 토큰입니다."):
        return cls(401, "JWT_EXPIRED", message)

    @classmethod
    def jwt_unsupported(cls, message: str = "지원되지 않는 JWT 토큰입니다."):
        return cls(401, "JWT_UNSUPPORTED", message)

    @classmethod
    def jwt_claim_empty(cls, message: str = "JWT 토큰이 잘못되었습니다."):
        return cls(401, "JWT_CLAIM_EMPTY", message)

    @classmethod
    def jwt_invalid(cls, message: str = "유효하지 않은 JWT 토큰입니다."):
        return cls(401, "JWT_INVALID", message)