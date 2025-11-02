from app.core.config import setting, redis_settings
from app.core.start_up.bootstrap import init
from app.api.deps import get_extractor
from app.api.routers import auth_controller, books_controller, user_controller, categories_controller, health_controller, stats_controller
from app.services.extract import ExtractService
from fastapi import FastAPI

init()
extractor: ExtractService = get_extractor()
extractor.extract_and_save_books()

app = FastAPI(
    title = setting.SERVICE_NAME,
    version = setting.VERSION,
    description = setting.DESCRIPTION
)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(books_controller.router)
app.include_router(categories_controller.router)
app.include_router(health_controller.router)
app.include_router(stats_controller.router)

@app.on_event("shutdown")
async def shutdown():
    await redis_settings.RedisConnection.close()