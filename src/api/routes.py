import logging

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from src.db.database_services import count_records_in_tables

logger = logging.getLogger(__name__)

api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"hellow": "world"}


@api_router.get("/count", status_code=status.HTTP_200_OK)
async def count():
    count = count_records_in_tables()
    return count
