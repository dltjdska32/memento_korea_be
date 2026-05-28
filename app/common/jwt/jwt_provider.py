from datetime import datetime, timezone, timedelta

import jwt
from jwt import InvalidSignatureError, DecodeError, ExpiredSignatureError, InvalidTokenError

from app.common.jwt.jwt_exception import JwtException
from app.common.jwt.jwt_settings import jwt_settings

from app.common.config.global_const import (
    JWT_CLAIM_EMAIL,
    JWT_CLAIM_ROLE,
    JWT_CLAIM_USERNAME,
    REFRESH_TOKEN_COOKIE_KEY,
)
from app.common.jwt.jwt_user_info import JwtUserInfo


class JwtProvider:
    def __init__(self):
        self._secret = jwt_settings.jwt_secret
        self._access_exp = jwt_settings.jwt_access_exp
        self._refresh_exp = jwt_settings.jwt_refresh_exp
        self._algorithm = jwt_settings.jwt_algorithm


    # 엑세스토큰 생성.
    def create_access_token(self,
                            user_id: int,
                            user_name: str,
                            email: str,
                            role: str) -> str:

        now = datetime.now(timezone.utc)
        exp = now + timedelta(milliseconds=self._access_exp)

        payload = {
            "sub": str(user_id),
            JWT_CLAIM_USERNAME: user_name,
            JWT_CLAIM_EMAIL: email,
            JWT_CLAIM_ROLE: role,
            "iat": now,
            "exp": exp
        }

        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    # 리프레시토큰 생성
    def create_refresh_token(self,
                             user_id: int) -> str:

        now = datetime.now(timezone.utc)
        exp = now + timedelta(milliseconds=self._refresh_exp)

        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": exp
        }

        return jwt.encode(payload, self._secret, algorithm=self._algorithm)


    # 웹 용 - 앱 전용서버면 사용 x
    def save_refresh_token_to_cookie(self,
                                     response,
                                     refresh_token: str) -> None:

        max_age = self._refresh_exp // 1000

        response.set_cookie(
            key=REFRESH_TOKEN_COOKIE_KEY,
            value=refresh_token,
            httponly=True,
            secure=False,  # prod: True
            path="/",
            max_age=max_age,
        )


    # 리프레시토큰 제거
    def delete_refresh_token_from_cookie(self,
                                         response,) -> None:
        response.set_cookie(
            key=REFRESH_TOKEN_COOKIE_KEY,
            value="",
            httponly=True,
            secure=True,
            path="/",
            max_age=0,
        )

    # 토큰 검증.
    def validate_token(self,
                       token: str,) -> None:

        try:
            jwt.decode(token,
                       self._secret,
                       algorithms=[self._algorithm])

        except InvalidSignatureError | DecodeError:
            raise JwtException.jwt_invalid_malformed()
        except ExpiredSignatureError:
            raise JwtException.jwt_expired()
        except InvalidTokenError:
            raise JwtException.jwt_unsupported()
        except Exception:
            raise JwtException.jwt_invalid()


    # 클레임 조회
    def get_claims(self,
                   token: str,) -> dict:

        self.validate_token(token)

        return jwt.decode(
            token,
            self._secret,
            algorithms=[self._algorithm],
        )


    def get_jwt_user_info(self, token: str) -> JwtUserInfo:
        claims = self.get_claims(token)

        sub = claims.get("sub")
        username = claims.get(JWT_CLAIM_USERNAME)
        email = claims.get(JWT_CLAIM_EMAIL)
        role = claims.get(JWT_CLAIM_ROLE)

        if not all([sub, username, email, role]):
            raise JwtException.jwt_claim_empty("JWT 유저 정보를 확인할 수 없음.")

        return JwtUserInfo(
            user_id=int(sub),
            username=username,
            email=email,
            role=role,
        )