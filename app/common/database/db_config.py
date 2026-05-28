from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.common.database.db_settings import db_settings
# db 설정 및 sql아키미 설정

# 포스트그리 비동기 연결풀 생성
engine = create_async_engine(
    db_settings.db_url,
    echo=True,              # SQL 로그 출력  -> true 출력 , false 출력 x
    pool_size=5,            # 풀 사이즈
    max_overflow=7,         # 5개 풀일경우 7개 추가 사용가능
    pool_pre_ping=True,     # 끊긴 연결 자동 갱신
)


# 디비 세션 생성 함수
async_session = async_sessionmaker(
    bind=engine,            # 어느 DB 사용할지 설정
    class_=AsyncSession,    # 비동기 사용
    expire_on_commit=False, # 커밋후 객체 데이터 사용 DB 조회 x
)