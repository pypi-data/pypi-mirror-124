"""
Работа с файлами:
    - поиск всех файлов-конспектов и получение их имен
"""

import os
import sys

from abstract_builder import loger

ROOT_CATALOG = ""
EXTENSION = "h"


def getFilesList(root_catalog):
    """
    возвращает список result путей к файлам конспектов относительно корневого каталога
    """

    ROOT_CATALOG = root_catalog

    loger.Loger.log_str(module_name="expfile", location="getFilesList", text="Начало обработки файлов в каталоге:")
    loger.Loger.log_str(module_name="expfile", location="getFilesList", text=ROOT_CATALOG)

    result = []

    loger.Loger.log_str(module_name="expfile", location="getFilesList", text="Список найденных файлов:")

    for catalog, subdirs, files in os.walk(ROOT_CATALOG):

        # каталоги, в которых не нужно искать конспекты
        exceptions = ["node_modules"]

        is_exception = False

        for exception in exceptions:
            if catalog.find(exception) != -1:
                is_exception = True

        if is_exception is True:
            continue

        # производится поиск файлов
        for file in files:
            file_spl = file.split(".")

            # если файл нужного нам расширения
            if file_spl[-1] == EXTENSION:
                fullname = os.path.join(catalog, file)

                loger.Loger.log_str(module_name="expfile", location="getFilesList", text=fullname)
                result.append(fullname)

    if len(result) == 0:
        loger.Loger.log_str(module_name="expfile", location="getFilesList", text="не найден ни один файл")

    return result

