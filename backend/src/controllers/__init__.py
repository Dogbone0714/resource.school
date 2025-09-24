from .auth_controller import auth_router
from .upload_controller import upload_router
from .pdf_controller import pdf_router
from .recommendation_controller import recommendation_router
from .resource_controller import resource_router

__all__ = [
    "auth_router",
    "upload_router",
    "pdf_router",
    "recommendation_router", 
    "resource_router"
]
