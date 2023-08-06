import os
import sys

import os.path
from importlib import resources

from abstract_builder import expfile
from abstract_builder import interpretator
from abstract_builder import loger

# каталог, в который будут сохраняться готовые файлы
RESULT_CATALOG = os.path.join(expfile.ROOT_CATALOG, "docs")
RESULT_CATALOG_RES = os.path.join(RESULT_CATALOG, "static")


def copyStaticFiles(file_name):
    # создание каталога для готовых файлов
    if not os.path.exists(RESULT_CATALOG):
        os.mkdir(RESULT_CATALOG)

    if not os.path.exists(RESULT_CATALOG_RES):
        os.mkdir(RESULT_CATALOG_RES)

    lines = []

    data_dir = os.path.join(os.path.dirname(__file__), 'static')
    data_path = os.path.join(data_dir, file_name)

    with open(data_path, encoding="utf-8") as res_file:
        lines = res_file.readlines()

    out_file = open(os.path.join(RESULT_CATALOG_RES, file_name), "w", encoding="utf-8")

    for line in lines:
        out_file.write(line)

    out_file.close()


def process(file_list):
    for filename in file_list:

        loger.Loger.log_str(module_name="main", location="process", text="Начало обработки файла: " + filename)

        copyStaticFiles("style.css")
        copyStaticFiles("main.js")

        # название файла без расширения
        base_name = os.path.basename(filename).split(".")[0]

        # открытие файлов для чтения и записи
        in_file = open(filename, "r", encoding="utf-8")
        out_file = open(os.path.join(RESULT_CATALOG, base_name + ".html"), "w", encoding="utf-8")

        # считывание файла построчно в список
        current_file_lines = []

        while True:
            line = in_file.readline()

            if not line:
                break

            current_file_lines.append(line)

        # получение HTML-документа и запись в файл
        interp = interpretator.Interpretator()
        interp.setSourse(current_file_lines)

        result = interp.getHtml()

        out_file.write(result)

        # закрытие файлов
        in_file.close()
        out_file.close()


def build(root_catalog):
    # список файлов конспектов
    files = expfile.getFilesList(root_catalog)

    process(files)

