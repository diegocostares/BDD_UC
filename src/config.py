import enum
import logging
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from pydantic import validator
from pydantic_settings import BaseSettings

# Definición de códigos de color ANSI
COLORS = {
    "DEBUG": "\033[94m",
    "INFO": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "CRITICAL": "\033[31m",
    "ENDC": "\033[0m",
}
TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = f"{COLORS.get(record.levelname, COLORS['ENDC'])}{record.levelname}{COLORS['ENDC']}"
        return super().format(record)


class AppConfig(BaseSettings):
    # Application configuration
    environment: str = "dev"
    log_level: LogLevel = LogLevel.INFO
    log_file: Optional[str] = None
    host: str = "localhost"
    port: int = 8000
    api_base_path: Path = Path("/api")
    # Database configuration
    db_scheme: str = "postgresql"
    db_name: str = "database"
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432

    @validator("environment")
    def check_environment(cls, value):
        if value not in ["dev", "prod"]:
            raise ValueError('Environment must be either "dev" or "prod"')
        return value

    def configure_logging(self):
        level = self.log_level.value
        numeric_level = getattr(logging, level, None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {level}")

        formatter = ColoredFormatter("%(levelname)s: \t\t%(asctime)s - %(name)s - %(message)s")
        handlers = []
        if self.log_file:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

        logger = logging.getLogger("bdd_uc")
        logger.setLevel(numeric_level)
        for handler in handlers:
            logger.addHandler(handler)
        logger.propagate = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = AppConfig()
config.configure_logging()

# Ejemplo de uso en otro archivo del proyecto:
# logger = logging.getLogger(__name__)
# logger.info("Starting the application.")
