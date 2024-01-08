import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from ..config import config
from .models import (
    Base,
    CourseCatalog,
    CourseSection,
    CourseSectionBannerVacancy,
    CourseSectionSchedule,
    CourseTeacher,
    Teacher,
    VacancyDetail,
)

logger = logging.getLogger("bdd_uc")


def get_engine(user: str, password: str, db_name: str, host: str, driver: str = "postgresql"):
    return create_engine(f"{driver}://{user}:{password}@{host}/{db_name}")


def create_database_if_not_exists(engine):
    if not database_exists(engine.url):
        create_database(engine.url)


engine = get_engine(
    user=config.db_user,
    password=config.db_password,
    db_name=config.db_name,
    host=config.db_host,
    driver=config.db_scheme,
)

create_database_if_not_exists(engine)
Session = sessionmaker(bind=engine)


def create_db(clean: bool = False):
    if clean:
        logger.debug("Dropping all tables")
        Base.metadata.drop_all(engine)
    logger.debug("Creating all tables")
    Base.metadata.create_all(engine)


# create_db(clean=True)  # TODO: traspasar a la API
