from functools import lru_cache

from app.common.jwt.jwt_provider import JwtProvider

# jwt 의존성 주입용 함수.
# spring 의 @Bean 역할.
@lru_cache
def get_jwt_provider() -> JwtProvider:
    return JwtProvider()
