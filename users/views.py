from fastapi import APIRouter
from .shemas import CreateUser
from users import cruds

router = APIRouter(prefix="/users")


@router.post("/")
def create_user(user: CreateUser):
    return cruds.create_user(user)
