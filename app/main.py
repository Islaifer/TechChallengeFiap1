from app.core.config import setting, redis_settings
from app.core.start_up.bootstrap import init
from app.api.routers import auth_controller
from app.api.routers import user_controller
from app.api.routers import books_controller
from app.api.routers import stats_controller
from fastapi import FastAPI

init()

app = FastAPI(
    title = setting.SERVICE_NAME,
    version = setting.VERSION,
    description = setting.DESCRIPTION
)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(books_controller.router)
app.include_router(stats_controller.router)

@app.on_event("shutdown")
async def shutdown():
    await redis_settings.RedisConnection.close()