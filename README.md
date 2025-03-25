<p align="center">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="center" width="30%">
</p>
<p align="center"><h1 align="center"><code>❯ FizHub </code></h1></p>
<p align="center">
	<em><code>❯ S3 stub </code></em>
</p>
<p align="center">
	<!-- local repository, no metadata badges. --></p>
<p align="center">Используемые технологии</p>
<p align="center">
	<img src="https://img.shields.io/badge/Jinja-B41717.svg?style=default&logo=Jinja&logoColor=white" alt="Jinja">
	<img src="https://img.shields.io/badge/NGINX-009639.svg?style=default&logo=NGINX&logoColor=white" alt="NGINX">
	<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=default&logo=FastAPI&logoColor=white" alt="FastAPI">
	<img src="https://img.shields.io/badge/Pytest-0A9EDC.svg?style=default&logo=Pytest&logoColor=white" alt="Pytest">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=default&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=default&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/AIOHTTP-2C5BB4.svg?style=default&logo=AIOHTTP&logoColor=white" alt="AIOHTTP">
	<img src="https://img.shields.io/badge/Pydantic-E92063.svg?style=default&logo=Pydantic&logoColor=white" alt="Pydantic">
</p>
<br>

##  Оглавление
- [Введение](#описание)
- [Особенности](#особенности)
- [Структура проекта](#структура-проекта)
- [Начало работы](#начало-работы)
  - [Установка](#установка)
  - [Запуск](#запуск)
---

##  Описание

<code>
Данный проект выступает в качестве заглушки S3 хранилища.

Сервис написан на FastAPI.
</code>

---

##  Особенности

<code>
Используется Docker для развертывания проекта на сервере.

Для локальной работы достаточно запустить **app.py**
</code>

---

##  Структура проекта

```sh
└── /
    ├── Dockerfile
    ├── README.md
    ├── app.py
    ├── docker-compose.yml
    ├── nginx
    │   └── nginx.conf
    ├── rabbitmq.py
    ├── requirements.txt
    └── storage.py
```

##  Начало работы

###  Установка


1. Клонируйте репозиторий:
```sh
❯ git clone ../
```

2. Перейдите в папку с проектом:
```sh
❯ cd 
```

3. Установка зависимостей:


**Используя `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```


**Используя `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker compose build
```

###  Запуск
Для локального использования:

```sh
❯ python app.py
```

Для запуска на сервере:
```sh
❯ docker compose up 
```


