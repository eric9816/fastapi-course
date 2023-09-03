from fastapi import APIRouter, HTTPException, status, Response

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.service import UserService
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"]
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    # response - класс для ответов пользователю

    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({'sub': str(user.id)})

    # Отправляем куки в браузер клиента
    response.set_cookie("booking_access_token", access_token, httponly=True)  # http_only - флаг, которые не позволит забрать куки через JS
    return {'access_token': access_token}