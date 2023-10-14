import aioredis
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database import db
from app.config import settings
from fastapi import FastAPI
from app.routes import user_routes, room_routes, photo_room_routes

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


app.include_router(user_routes.router)
app.include_router(room_routes.router)
app.include_router(photo_room_routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
