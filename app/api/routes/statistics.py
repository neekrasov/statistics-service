from fastapi import APIRouter

router = APIRouter(prefix='', tags=['statistics'])

@router.get("/stat")
async def show_stat():
    return {"": ""}

@router.post("/add")
async def add_stat():
    return {"": ""}

@router.post("/remove")
async def remove_stat():
    return {"": ""}