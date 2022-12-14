from fastapi import FastAPI

from app.celery import create_celery
from app.users.views import users_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(users_router)

    return app


app = create_app()

celery = create_celery()


@app.get("/")
async def root():
    return {"message": "Hello World"}
