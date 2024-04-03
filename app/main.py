from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

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

    add_exception_handlers(app)
    init_views(app)

    return app


app = create_app()
