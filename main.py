from fastapi import FastAPI

from app.broadcast_utils import broadcast
from app.celery_utils import create_celery
from app.users.views import users_router
from app.ws.views import ws_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(users_router)
    app.include_router(ws_router)

    @app.on_event("startup")
    async def startup_event():
        await broadcast.connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        await broadcast.disconnect()

    return app


app = create_app()

celery = create_celery()


@app.get("/")
async def root():
    return {"message": "Hello World"}
