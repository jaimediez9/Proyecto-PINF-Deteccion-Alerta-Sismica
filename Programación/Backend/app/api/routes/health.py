#Para comprobar que todo va bien
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "app sin nombre todavia. Backend"
    }