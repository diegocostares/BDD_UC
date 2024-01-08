import time

import scrapy

from src.db.database_services import get_nrcs_from_bd
from src.scraper.items import CourseVacancyItem
from src.scraper.utils import current_semester

from ...config import config


class CourseVacancyScraper(scrapy.Spider):
    name = "coursevacancyscraper"
    allowed_domains = ["proxy-buscacursos-diego-costa-dg2vxpylqa-uc.a.run.app"]

    def __init__(self, banner=None, *args, **kwargs):
        super(CourseVacancyScraper, self).__init__(*args, **kwargs)
        self.banner = banner
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def start_requests(self):
        base_url = "https://proxy-buscacursos-diego-costa-dg2vxpylqa-uc.a.run.app/informacionVacReserva.ajax.php"
        if config.environment == "dev":
            nrcs = ["12241", "12247", "12251", "12256", "12262", "12267", "12271", "12276", "12282", "23690", "24169"]
        else:
            nrcs = get_nrcs_from_bd()
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
            item["banner"] = self.banner
            item["date"] = self.date
            yield item


def safe_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default
