from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.organizations import router as organizations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    allow_origins=["*"],
)

app.include_router(organizations_router)
