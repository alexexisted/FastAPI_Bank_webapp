from fastapi import FastAPI
from core.config import settings
from db.base import Base
from db.session import engine
from apis.base import api_router


#i made create_tables function to create tables in database when application starts
def create_tables():
    Base.metadata.create_all(bind=engine)

# simple function to include routers in main.py, also it's a good way to avoid the mess in code
def include_router(app):
    app.include_router(api_router)

# function to start application and start up all functions above
def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app

app = start_application()

@app.get("/")
def hello_api():
    return {"message": "We are not going to scam you"}
