from app.core.config import setting
from app.core.start_up.bootstrap import init
from app.api.routers import auth_controller
from app.api.routers import user_controller
from fastapi import FastAPI

init()

app = FastAPI(
    title = setting.SERVICE_NAME,
    version = setting.VERSION,
    description = setting.DESCRIPTION
)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
