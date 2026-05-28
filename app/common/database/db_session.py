from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from app.common.database.db_config import async_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:

    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise