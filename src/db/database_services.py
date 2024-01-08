from sqlalchemy.orm import sessionmaker

from src.db import engine
from src.db.models import (
    CourseCatalog,
    CourseSection,
    CourseSectionBannerVacancy,
    CourseSectionSchedule,
    CourseTeacher,
    Teacher,
    VacancyDetail,
)

Session = sessionmaker(bind=engine)


def get_nrcs_from_bd():
    session = Session()
    try:
        nrcs = session.query(CourseSection.nrc).all()
        nrc_list = [nrc[0] for nrc in nrcs]
        return nrc_list
    except Exception as e:
        print(f"Error al obtener nrcs: {e}")
        return []
    finally:
        session.close()


def count_records_in_tables():
    session = Session()
    try:
        count_course_catalog = session.query(CourseCatalog).count()
        count_course_section = session.query(CourseSection).count()
        count_course_section_banner_vacancy = session.query(CourseSectionBannerVacancy).count()

        return {
            "CourseCatalog": count_course_catalog,
            "CourseSection": count_course_section,
            "CourseSectionBannerVacancy": count_course_section_banner_vacancy,
        }
    except Exception as e:
        print(f"Error al contar registros: {e}")
        return {}
    finally:
        session.close()


if __name__ == "__main__":
    nrcs = get_nrcs_from_bd()
    print(nrcs)
    conteos = count_records_in_tables()
    print(conteos)
