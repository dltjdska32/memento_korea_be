from pydantic import BaseModel

from app.common.jwt.jwt_user_info import JwtUserInfo


class AuthUserInfo(BaseModel):
    user_id: int
    username: str
    email: str
    role: str

    @staticmethod
    def from_jwt(jwt_user_info: JwtUserInfo) -> "AuthUserInfo":
        return AuthUserInfo(
            user_id=jwt_user_info.user_id,
            username=jwt_user_info.username,
            email=jwt_user_info.email,
            role=jwt_user_info.role,
        )