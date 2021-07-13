from fastapi import APIRouter

router = APIRouter()


@router.get("/book/", tags=["book"])
def book():
    """Book room"""
    return {"test": "test"}
