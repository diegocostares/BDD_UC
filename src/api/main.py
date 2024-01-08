import asyncio
import logging
import subprocess
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import api_router
from src.banners_info import banners_info
from src.config import config
from src.db import create_db

logger = logging.getLogger("bdd_uc")

logger.info("Starting the application.\n\n\n")
app = FastAPI(
    # root_path=str(config.api_base_path), # TODO: ver por que no se puede accerder a api/docs
    title="BDD UC",
    description="Base De Datos Unificada y Comunitaria",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = AsyncIOScheduler()


async def run_spider(spider_name, banner=None):
    command = ["poetry", "run", "scrapy", "crawl", spider_name]
    if banner is not None:
        command += ["-a", f"banner={banner}"]
    await asyncio.create_subprocess_exec(*command)


@app.on_event("startup")
def on_startup():
    logger.info("Database starting...")
    create_db()

    logger.info("Starting jobs...")
    for time_str, (spider, banner) in banners_info.items():
        run_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        scheduler.add_job(run_spider, "date", run_date=run_time, args=[spider, banner])

    scheduler.start()


app.include_router(api_router, prefix=str(config.api_base_path))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:create_app",
        factory=True,
        workers=config.workers_count,
        host=config.host,
        # port=config.port,
        reload=True,
        log_level=config.log_level.value.lower(),
    )
