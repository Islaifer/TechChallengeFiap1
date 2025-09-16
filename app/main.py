from app.core.config import setting
from app.core.start_up.bootstrap import init
from app.api.routers import auth
from fastapi import FastAPI

init()

app = FastAPI(
    title = setting.SERVICE_NAME,
    version = setting.VERSION,
    description = setting.DESCRIPTION
)

app.include_router(auth.router)
