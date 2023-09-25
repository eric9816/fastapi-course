import time
import sentry_sdk

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_image
from app.pages.router import router as router_pages
# from app.users.models import Users
from app.users.router import router as router_users
from app.logger import logger
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# sentry_sdk.init(
#     dsn="https://f5a83394c84ed5f3a4e5952fc7156672@o4505934709325824.ingest.sentry.io/4505934714372096",
#     traces_sample_rate=1.0,
#     profiles_sample_rate=1.0,
# )


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_image)

# Инициализация CORS
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # чтобы с фронта куки могли приходить на бек и мы могли бы авторизовать его
    allow_methods=["*"],
    allow_headers=["*"],
)


# Запуск Редиса при старте приложения
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# Версионирование API
app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}',
                       # description='Greet users with a nice message',
                       # middleware=[
                       #     Middleware(SessionMiddleware, secret_key='mysecretkey')
                       # ]
                       )

# монтирование - добавляем отдельного приложение для картинок
app.mount("/static", StaticFiles(directory="app/static"), "static")

# АДМИНКА
admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)


# Middleware для обработки запросов от пользователя для дальнейшего логгирования
# В данном случае можно добавить время обработки запросов, при помощи time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)  # Тут вызывается любая вьюшка, на которую делается запрос
    process_time = time.time() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response


# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
