from app.core.config import setting, redis_settings
from app.core.start_up.bootstrap import init
from app.api.deps import get_extractor
from app.api.routers import auth_controller, books_controller, user_controller, categories_controller, health_controller, stats_controller
from app.services.extract import ExtractService
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

init()
extractor: ExtractService = get_extractor()
extractor.extract_and_save_books()

app = FastAPI(
    title = setting.SERVICE_NAME,
    version = setting.VERSION,
    description = setting.DESCRIPTION
)

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title = setting.SERVICE_NAME,
        version = setting.VERSION,
        description = setting.DESCRIPTION,
        routes=app.routes,
    )
    # Garante que 'components' existe
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    # Agora é seguro adicionar o esquema de segurança
    openapi_schema["components"]["securitySchemes"] = {
        "Auth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Aplica o esquema globalmente (opcional)
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(books_controller.router)
app.include_router(categories_controller.router)
app.include_router(health_controller.router)
app.include_router(stats_controller.router)

@app.on_event("shutdown")
async def shutdown():
    await redis_settings.RedisConnection.close()