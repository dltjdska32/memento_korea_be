from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.common.auth.auth_middleware import AuthMiddleware
from app.common.auth.auth_settings import auth_settings
from app.common.exception.exception_handler import register_exception_handlers
from app.common.jwt.jwt_dependency import get_jwt_provider
from app.common.redis.redis_config import init_redis, close_redis


# 앱시작시 레디스 연결 종료시 커넥션 끊음
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()  
    yield
    await close_redis()
app = FastAPI(lifespan=lifespan)

# 요청 처리 : 클라 -> cors -> auth -> 엔드포인트

app.add_middleware(
    AuthMiddleware,
    jwt_provider=get_jwt_provider(),        # authMiddelware 파람1
    whitelist=auth_settings.api_whitelist,  # authMiddelware 파람2
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, # 쿠키/인증 헤더 포함 요청 -> 운영시 오리진스*과 크리덴셜 true 같이 사용불가 도메인 명시 필요.
    allow_methods=["*"],
    allow_headers=["*"],
)



register_exception_handlers(app)