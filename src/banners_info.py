"""
Archivo para generar la lista de banners y horarios que se ejecutaran en el scheduling
"""

horarios = ["08:40", "10:10", "11:40", "13:10", "14:40", "16:10", "17:40", "19:10"]
################################################################
# Primera vuelta
################################################################
banners_info = {  # TODO: Configurar en el futuro con los horarios generales
    "2024-01-08 02:23": ("generalbuscacursos", None),
    "2024-01-08 07:45": ("coursevacancyscraper", "None"),
    "2024-01-08 08:40": ("coursevacancyscraper", "1"),
    "2024-01-08 10:10": ("coursevacancyscraper", "2"),
    "2024-01-08 11:40": ("coursevacancyscraper", "3"),
    "2024-01-08 13:10": ("coursevacancyscraper", "4"),
    "2024-01-08 14:40": ("coursevacancyscraper", "5"),
    "2024-01-08 16:10": ("coursevacancyscraper", "6"),
    "2024-01-08 17:40": ("coursevacancyscraper", "7"),
    "2024-01-08 19:10": ("coursevacancyscraper", "8"),
    "2024-01-09 08:40": ("coursevacancyscraper", "9"),
    "2024-01-09 10:10": ("coursevacancyscraper", "10"),
    "2024-01-09 11:40": ("coursevacancyscraper", "11"),
    "2024-01-09 13:10": ("coursevacancyscraper", "12"),
    "2024-01-09 14:40": ("coursevacancyscraper", "13"),
    "2024-01-09 16:10": ("coursevacancyscraper", "14"),
    "2024-01-09 17:40": ("coursevacancyscraper", "15"),
    "2024-01-09 19:10": ("coursevacancyscraper", "16"),
}


################################################################
# Segunda vuelta
################################################################
vueltas_adicionales = {
    "2024-01-10": list(range(1, 9)),
    "2024-01-11": list(range(9, 17)),
}
for fecha, banners in vueltas_adicionales.items():
    for hora, banner in zip(horarios, banners):
        banners_info[f"{fecha} {hora}"] = ("coursevacancyscraper", str(banner))

################################################################
# Primer reajuste
################################################################
vueltas_adicionales = {
    "2024-01-16": list(range(16, 8, -1)),
    "2024-01-17": list(range(8, 0, -1)),
}
for fecha, banners in vueltas_adicionales.items():
    for hora, banner in zip(horarios, banners):
        banners_info[f"{fecha} {hora}"] = ("coursevacancyscraper", str(banner))

################################################################
# Segundo reajuste
################################################################
for i, hora in enumerate(horarios):
    banner1 = 2 * i + 1
    banner2 = 2 * i + 2
    banners_info[f"2024-01-19 {hora}"] = ("coursevacancyscraper", f"{banner1} y {banner2}")


if __name__ == "__main__":
    for key, value in banners_info.items():
        print(f"{key}: {value}")
