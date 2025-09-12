from app.core.config import setting
from app.api.routers import auth
from fastapi import FastAPI

app = FastAPI(
    title = setting.SERVICE_NAME,
    version = setting.VERSION,
    description = setting.DESCRIPTION
)

app.include_router(auth.router)
