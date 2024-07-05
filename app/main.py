from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.schemas.user import SignUpRequest
from app.db import get_async_session
from app.db.user_model import UserModel

app = FastAPI()

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

origins = ["http://localhost:3000", "http://localhost", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": settings.POSTGRES_DB,
    }


@app.post("/add_user")
async def add_user(
    user: SignUpRequest, session: AsyncSession = Depends(get_async_session)
):

    new_user = UserModel(
        email=user.email, username=user.username, hashed_password=user.password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
