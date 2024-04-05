import asyncio

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from typing import Any, AsyncGenerator, AsyncIterator, Generator
from app.base.db import Base
from app.base.config import settings
from asgi_lifespan import LifespanManager
from app.deps import session as session_dependency


import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app
from app.repositories.user import UserRepository
from app.services.user import UserService
import sqlalchemy as sa
from sqlalchemy_utils import create_database
from sqlalchemy.exc import ProgrammingError


@pytest.fixture(scope="session")
def event_loop() -> Generator[Any, Any, Any]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> Generator[None, None, None]:
    engine = sa.create_engine(settings.db_url.replace("+asyncpg", ""))
    try:
        create_database(engine.url)
    except ProgrammingError:
        pass
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    # create_database(engine.url)
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
async def engine(setup_database: None) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(settings.db_url)
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    conn = await engine.connect()
    trans = await conn.begin()
    session = AsyncSession(bind=conn, expire_on_commit=False)
    yield session
    if session.is_active:
        await trans.rollback()
    await session.close()
    await conn.close()


@pytest.fixture(scope="session")
async def initialized_app() -> AsyncGenerator[Any, Any]:
    app = create_app()
    async with LifespanManager(app):
        yield app


@pytest.fixture(scope="session")
async def client(initialized_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=initialized_app),
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def clear_app_dependency_override(
    initialized_app: FastAPI, session: AsyncSession
) -> Generator[None, Any, None]:
    initialized_app.dependency_overrides[session_dependency] = lambda: session
    yield
    initialized_app.dependency_overrides = {}


@pytest.fixture
def user_repo(session: AsyncSession) -> UserRepository:
    return UserRepository(session)


@pytest.fixture
def user_service(user_repo: UserRepository) -> UserService:
    return UserService(user_repo)
