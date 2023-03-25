from fastapi import APIRouter

router = APIRouter(
    tags= ['Users']
)

@router.get("/")
async def register_user():
    pass

@router.post("/")
async def register_user():
    pass