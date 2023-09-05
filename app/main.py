import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from app.images.router import router as router_image

app = FastAPI()

# монтирование - добавляем отдельного приложение
app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_image)

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)