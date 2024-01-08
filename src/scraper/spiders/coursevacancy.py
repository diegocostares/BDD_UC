import scrapy

from src.scraper.items import CourseVacancyItem
from src.scraper.utils import current_semester


def obtener_nrcs_de_bd():
    # TODO
    return ["22392"]


class CourseVacancyScraper(scrapy.Spider):
    name = "course_vacancy_scraper"
    allowed_domains = ["proxy-buscacursos-diego-costa-dg2vxpylqa-uc.a.run.app"]

    def start_requests(self):
        base_url = "https://proxy-buscacursos-diego-costa-dg2vxpylqa-uc.a.run.app/informacionVacReserva.ajax.php"
        nrcs = obtener_nrcs_de_bd()
        term = current_semester()

        for nrc in nrcs:
            url = f"{base_url}?nrc={nrc}&termcode={term}"
            yield scrapy.Request(url, self.parse, cb_kwargs={"nrc": nrc})

    def parse(self, response, nrc):
        rows = response.xpath(
            "/html/body/table/tbody/tr[position()>4 and not(position()=last()) and not(position()=last()-1)]"
        )
        for row in rows:
            item = CourseVacancyItem()
            item["nrc"] = nrc
            item["school"] = row.xpath("td[1]/text()").get().strip()
            item["level"] = row.xpath("td[2]/text()").get().strip()
            item["program"] = row.xpath("td[3]/text()").get().strip()
            item["concentration"] = row.xpath("td[4]/text()").get().strip()
            item["cohort"] = row.xpath("td[5]/text()").get().strip()
            item["admission_period"] = row.xpath("td[6]/text()").get().strip()
            item["offered"] = safe_int(row.xpath("td[7]/text()").get().strip())
            item["occupied"] = safe_int(row.xpath("td[8]/text()").get().strip())
            item["available"] = safe_int(row.xpath("td[9]/text()").get().strip())

            yield item


def safe_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default
