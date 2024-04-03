from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.requests import Request


from app.exceptions import NotFoundError, PermissionError, ValidationError


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(PermissionError, permission_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(NotFoundError, notfound_error_handler)


def permission_error_handler(request: Request, exc: Exception) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=403,
        content={"message": str(exc)},
    )


def notfound_error_handler(request: Request, exc: Exception) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=404,
        content={"message": str(exc)},
    )


def validation_error_handler(request: Request, exc: Exception) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=409,
        content={"message": str(exc)},
    )
