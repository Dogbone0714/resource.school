from fastapi import APIRouter
from ..controllers import (
    auth_router,
    upload_router,
    recommendation_router,
    resource_router
)

main_router = APIRouter()

# 包含所有子路由
main_router.include_router(auth_router)
main_router.include_router(upload_router)
main_router.include_router(recommendation_router)
main_router.include_router(resource_router)
