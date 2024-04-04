from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from typing import Awaitable, Callable
from app.base.db import db

from app.exception_handlers import add_exception_handlers

NO_DB_ROUTES = {"/ping", "/openapi.json", "/docs", "/redoc"}


def init_views(app: FastAPI) -> None:
    from app.views import router as v1_router

    @app.get("/")
    def ping() -> str:
        return "Hello, Unithon!"

    app.include_router(v1_router, prefix="/v1")


def create_app() -> FastAPI:
    """FastAPI 앱을 생성합니다."""

    app = FastAPI(
        openapi_url="/openapi.json",
        default_response_class=ORJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],  # TODO: 배포시에는 특정 도메인만 허용하도록 변경 필요.
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def db_session_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """request마다 session을 유지하기 위해 사용"""
        if request.url.path in NO_DB_ROUTES:
            return await call_next(request)

        response = Response("Internal server error", status_code=500)
        async with db.session() as session:
            request.state.session = session
            response = await call_next(request)
        return response

    add_exception_handlers(app)
    init_views(app)

    return app


app = create_app()
