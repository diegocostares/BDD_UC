import scrapy
from scrapy.selector import Selector
from sqlalchemy.orm import sessionmaker

from src.db import engine
from src.db.models import Base, CourseCatalog, CourseSection

from .items import StartBuscacursosItem


class StartBuscacursosPipeline:
    def __init__(self):
        self.Session = None

    def open_spider(self, spider):
        if spider.name == "generalbuscacursos":
            print("Creando la base de datos")
            self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if self.Session is None or not isinstance(item, StartBuscacursosItem):
            return item
        session = self.Session()
        try:
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
            session.add(course_section)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        return item
