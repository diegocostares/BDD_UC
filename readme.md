# BDD UC

**Base De Datos Unificada y Comunitaria 📚**

## Requisitos

- Python >= 3.11
- Crear un archivo `.env` utilizando las variables definidas en `.ENV_TEMPLATE`

## Ejecución

```shell
# api
poetry run uvicorn src.api.main:app --reload
# scraper manual
poetry run scrapy crawl <spider_name> # Opcional: -o items.json
```

### Linter y Formatter

Para mantener la consistencia en el código y respetar el pep8, hay que instalar y usar ruff y black.

### Dependencias

Para listar las dependencias del proyecto usaremos poetry.

<details>
  <summary><strong>Instalación de Poetry</strong> (haz clic para expandir)</summary>

#### Linux, macOS, Windows (WSL):

Con brew:

```shell
brew install poetry
```

sin:

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

#### Windows (Powershell)

```shell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

</details>

```shell
brew install --cask chromedriver
```

#### Actualización de Dependencias

Para agregar nuevas dependencias, utiliza:

```shell
poetry add <nombre-del-paquete>
```

Y para actualizar las dependencias existentes:

```shell
poetry update
```

## Tareas:

- [] Actualizar `devcontainers` a la nueva estructura
- [] Actualizar `scripts` y revisar que se puede simplificar
- [] Actualizar documentación
- [] Agregar diagrama ER
- [] IMPORTANTE: Ver si usar `asyncio`

# Agradecimientos

- [Nicolás Mc](https://github.com/nico-mac)
- [Andrés aurmeneta](https://github.com/aurmeneta)
- [Benjamín Vicente](https://github.com/benjavicente)
- [Gabriel Faundez](https://github.com/FarDust)
- [Ignacio Porte Stefoni](https://github.com/IgnacioPorte)
- [Emmanuel Norambuena](https://github.com/eanorambuena)
- [Lucas Natero](https://github.com/lnatero)
- [Diego Costa](https://github.com/diegocostares)

## referencias

Otros proyectos de los cuales sirvieron de inspiración y estructura

- https://github.com/aurmeneta/HorarioUC
- https://github.com/aurmeneta/BuscaCursosUC/tree/master
