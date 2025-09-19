from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.schemas import ResourceCreate, ResourceResponse
from ..models.resource import Resource

resource_router = APIRouter(prefix="/api", tags=["資源管理"])

@resource_router.get("/resources", response_model=list[ResourceResponse])
async def get_resources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """獲取資源列表"""
    try:
        resources = db.query(Resource).offset(skip).limit(limit).all()
        return resources
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get resources: {str(e)}"
        )

@resource_router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    """獲取單一資源"""
    try:
        resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        return resource
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get resource: {str(e)}"
        )

@resource_router.post("/resources", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db)
):
    """建立新資源"""
    try:
        db_resource = Resource(**resource.dict())
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)
        return db_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create resource: {str(e)}"
        )

@resource_router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: int,
    resource: ResourceCreate,
    db: Session = Depends(get_db)
):
    """更新資源"""
    try:
        db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if not db_resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        for key, value in resource.dict().items():
            setattr(db_resource, key, value)
        
        db.commit()
        db.refresh(db_resource)
        return db_resource
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update resource: {str(e)}"
        )

@resource_router.delete("/resources/{resource_id}")
async def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    """刪除資源"""
    try:
        db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if not db_resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        db.delete(db_resource)
        db.commit()
        return {"message": "Resource deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete resource: {str(e)}"
        )
