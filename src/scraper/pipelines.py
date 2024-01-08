import scrapy
from scrapy.selector import Selector
from sqlalchemy.orm import sessionmaker

from src.db import engine
from src.db.models import (
    Base,
    CourseCatalog,
    CourseSection,
    CourseSectionBannerVacancy,
    CourseSectionSchedule,
    CourseTeacher,
    Teacher,
    VacancyDetail,
)

from .items import CourseVacancyItem, StartBuscacursosItem
from .utils import current_semester


class BasePipeline:
    def __init__(self, spider_name, item_class):
        self.Session = None
        self.spider_name = spider_name
        self.item_class = item_class

    def open_spider(self, spider):
        if spider.name == self.spider_name:
            self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if self.Session is None or not isinstance(item, self.item_class):
            return item
        session = self.Session()
        try:
            self.process_item_specific(item, session)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        return item

    def process_item_specific(self, item, session):
        raise NotImplementedError


class CourseVacancyPipeline(BasePipeline):
    def __init__(self):
        super().__init__("coursevacancyscraper", CourseVacancyItem)
        self.current_semester = current_semester()

    def process_item_specific(self, item, session):
        if "nrc" not in item or not self.current_semester:
            return
        course_section = (
            session.query(CourseSection).filter_by(nrc=item["nrc"], current_semester=self.current_semester).first()
        )
        if not course_section:
            return
        banner_vacancy = (
            session.query(CourseSectionBannerVacancy).filter_by(course_section_id=course_section.id).first()
        )
        if not banner_vacancy:
            banner_vacancy = CourseSectionBannerVacancy(
                course_section_id=course_section.id,
                banner=item.get("banner", 0),  # TODO: manejar banners
            )
            session.add(banner_vacancy)

        vacancy_detail = VacancyDetail(
            course_section_banner_vacancy_id=banner_vacancy.id,
            school=item["school"],
            level=item["level"],
            program=item["program"],
            concentration=item["concentration"],
            cohort=item["cohort"],
            admission_period=item["admission_period"],
            offered=item["offered"],
            occupied=item["occupied"],
            available=item["available"],
        )
        session.add(vacancy_detail)

        session.commit()


class StartBuscacursosPipeline(BasePipeline):
    def __init__(self):
        super().__init__("generalbuscacursos", StartBuscacursosItem)

    def process_item_specific(self, item, session):
        catalog = session.query(CourseCatalog).filter_by(code=item["code"]).first()
        if not catalog:
            catalog = CourseCatalog(
                name=item["general_area"],
                code=item["code"],
                credits=item["credits"],
            )
            session.add(catalog)

        course_section = CourseSection(
            nrc=item["nrc"],
            code=item["code"],
            allows_withdraw=item["allows_withdraw"],
            is_in_english=item["is_in_english"],
            section=item["section"],
            requires_special_approval=item["requires_special_approval"],
            fg_area=item["fg_area"],
            format=item["format"],
            category=item["category"],
            name=item["name"],
            campus=item["campus"],
            credits=item["credits"],
            current_semester=item["current_semester"],
            course_catalog=catalog,
        )
        # TODO: implementar logica de CourseTeacher, Teacher y CourseSectionSchedule
        session.add(course_section)
        session.commit()
