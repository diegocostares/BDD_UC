# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StartBuscacursosItem(scrapy.Item):
    """
    Si se quiere buscar el id hay que usar nrc y current_semester.
    """

    general_area = scrapy.Field()
    nrc = scrapy.Field()
    code = scrapy.Field()
    allows_withdraw = scrapy.Field()
    is_in_english = scrapy.Field()
    section = scrapy.Field()
    requires_special_approval = scrapy.Field()
    fg_area = scrapy.Field()
    format = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    teachers = scrapy.Field()  # TODO: por implementar
    campus = scrapy.Field()
    credits = scrapy.Field()
    total_vacancy = scrapy.Field()  # No se usa
    available_vacancy = scrapy.Field()  # No se usa
    reserved_vacancy = scrapy.Field()  # No se usa
    schedule = scrapy.Field()  # TODO: por implementar
    current_semester = scrapy.Field()


class CourseVacancyItem(scrapy.Item):
    nrc = scrapy.Field()
    school = scrapy.Field()
    level = scrapy.Field()
    program = scrapy.Field()
    concentration = scrapy.Field()
    cohort = scrapy.Field()
    admission_period = scrapy.Field()
    offered = scrapy.Field()
    occupied = scrapy.Field()
    available = scrapy.Field()
