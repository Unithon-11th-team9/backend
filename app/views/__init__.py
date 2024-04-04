from fastapi.routing import APIRouter

from app.views import user

router = APIRouter()

router.include_router(user.router, tags=["User"])
