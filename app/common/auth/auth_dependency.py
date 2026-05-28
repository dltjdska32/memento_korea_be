from fastapi import Request
from app.common.auth.auth_exception import AuthException
from app.common.auth.auth_user_info import AuthUserInfo

# 스프링의 @AuthenticationPrincipal 역할
async def get_current_user(request: Request) -> AuthUserInfo:
    user = getattr(request.state, "current_user", None)

    if user is None:
        raise AuthException.unauthorized()

    return user