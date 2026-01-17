from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL="postgresql+asyncpg://ayush:Ayush%40123@localhost:5432/task_manager"

engine=create_async_engine(
    DATABASE_URL,
    echo=False
)

AsyncSessionLocal=sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session