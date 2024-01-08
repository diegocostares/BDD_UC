import itertools
import warnings

import scrapy
from scrapy.exceptions import ScrapyDeprecationWarning

from src.scraper.items import StartBuscacursosItem
from src.scraper.utils import current_semester, generate_siglas

from ...config import config

warnings.filterwarnings("ignore", category=ScrapyDeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning, message=".*text and root.*")


class GeneralBuscacursosSpider(scrapy.Spider):
    """
    Araña que extrae las siglas y la informacion general del buscacursos.
    """

    name = "generalbuscacursos"
    current_semester = current_semester()
    allowed_domains = ["buscacursos.uc.cl", "proxy-buscacursos-diego-costa-dg2vxpylqa-uc.a.run.app"]

    def start_requests(self):
        """
        Crea una lista de urls para comenzar a buscar, variando el campus y las siglas que tiene.
        """
        if config.environment == "dev":
            campus_options = ["Casa Central"]
            siglas = ["MED"]
        elif config.environment == "prod":
            campus_options = ["Campus Externo", "Casa Central", "Lo Contador", "Oriente", "San Joaquín", "Villarrica"]
            siglas = generate_siglas()
        for campus, sigla in itertools.product(campus_options, siglas):
            url = f"https://proxy-buscacursos-diego-costa-dg2vxpylqa-uc.a.run.app/?cxml_semestre={self.current_semester}&cxml_campus={campus}&cxml_sigla={sigla}"
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={"sigla": sigla})

    def parse(self, response, sigla):
        """
        Si la búsqueda no produjo resultados, se devuelve un diccionario vacío.
        Si la búsqueda produjo demasiados resultados, se generan nuevas siglas y se vuelve a hacer la búsqueda.
        Si la búsqueda produjo resultados, se devuelve un diccionario con los resultados.
        """
        borde = response.xpath('//div[@class="bordeBonito"]/text()').get()

        if borde:
            if "La búsqueda no produjo resultados." in borde:
                yield {}
            elif "La búsqueda produjo demasiados resultados." in borde:
                nuevas_siglas = generate_siglas(sigla)
                for nueva_sigla in nuevas_siglas:
                    nueva_url = response.url.replace(f"cxml_sigla={sigla}", f"cxml_sigla={nueva_sigla}")
                    yield scrapy.Request(nueva_url, callback=self.parse, cb_kwargs={"sigla": sigla})
            else:
                self.logger.error(f"Error desconocido en la respuesta: {borde}")
        else:
            self.logger.debug(f"Capturando todos los resultados de {response.url}")
            general_area = None
            for row in response.xpath('//*[@id="wrapper"]/div/div/div[3]/table/tr'):
                if not row.xpath("@style") and not row.xpath("@class"):
                    general_area = row.xpath("./td[1]/text()").get().strip()
                elif "class" in row.attrib and (
                    "resultadosRowPar" in row.attrib["class"] or "resultadosRowImpar" in row.attrib["class"]
                ):
                    item = StartBuscacursosItem()
                    item["general_area"] = general_area
                    item["nrc"] = row.xpath("./td[1]/text()").get().strip()
                    item["code"] = row.xpath("./td[2]/div/text()").get().strip()
                    item["allows_withdraw"] = row.xpath("./td[3]/text()").get().strip()
                    item["is_in_english"] = row.xpath("./td[4]/text()").get().strip()
                    item["section"] = row.xpath("./td[5]/text()").get().strip()
                    item["requires_special_approval"] = row.xpath("./td[6]/text()").get().strip()
                    item["fg_area"] = row.xpath("./td[7]/text()").get().strip()
                    item["format"] = " ".join(row.xpath("./td[8]//text()").getall()).strip()
                    item["category"] = row.xpath("./td[9]/text()").get().strip()
                    item["name"] = row.xpath("./td[10]/text()").get().strip()
                    item["teachers"] = [t.strip() for t in row.xpath("./td[11]/a/text()").getall()]
                    item["campus"] = row.xpath("./td[12]/text()").get().strip()
                    item["credits"] = row.xpath("./td[13]/text()").get().strip()
                    item["total_vacancy"] = row.xpath("./td[14]/text()").get().strip()
                    item["available_vacancy"] = row.xpath("./td[15]/text()").get().strip()
                    item["reserved_vacancy"] = None
                    schedule = row.xpath("./td[17]/table/tr/td/text()").getall()
                    item["schedule"] = process_schedule(schedule)
                    item["current_semester"] = self.current_semester
                    yield item


def process_schedule(schedule_list):
    try:
        processed_schedule = []
        for i in range(0, len(schedule_list), 3):
            schedule_info = schedule_list[i].strip()
            schedule_type = schedule_list[i + 1].strip()
            classroom_info = schedule_list[i + 2].strip().strip("()")
            if schedule_info == ":":
                continue
            days, modules = schedule_info.split(":") if ":" in schedule_info else ("", "")
            days = days.split("-") if days else ["Unknown"]
            modules = modules.split(",") if modules else ["Unknown"]
            for day in days:
                for module in modules:
                    schedule_entry = {
                        "type": schedule_type,
                        "day": day,
                        "module": int(module) if module.isdigit() else "Unknown",
                        "classroom": classroom_info if classroom_info != "Por Asignar" else None,
                    }
                    processed_schedule.append(schedule_entry)
        return processed_schedule

    except Exception as e:
        print("Error en process_schedule:", e)
        print("Lista de horarios que causó el error:", schedule_list)
        return []
