from fastapi import FastAPI

from src.config import config
from src.db import create_db

app = FastAPI(root_path=str(config.api_base_path))


@app.on_event("startup")
def on_startup():
    create_db()
