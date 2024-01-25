from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from core.config import settings
from db.base import Base
from db.session import engine

from apis.base import api_router
from apps.base import app_router


#i made create_tables function to create tables in database when application starts
def create_tables():
    Base.metadata.create_all(bind=engine)

# simple function to include routers in main.py, also it's a good way to avoid the mess in code
def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)


def configure_staticfiles(app):
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# function to start application and start up all functions above
def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    configure_staticfiles(app)
    return app


app = start_application()


@app.get("/")
def hello_api():
    return {"message": "We are not going to scam you"}
