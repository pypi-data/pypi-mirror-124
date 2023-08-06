""" --------------------------------------------------------------------------------------------------------------------
Описывает класс интерпретатора.

--- parseLine(line)
--- parseTag(tag)

--- makeStringHtml(not_ready_string)
--- makeBlockHtml(head_element, content)

--- class NotReadyString

--- buildingData(index, head_element, data)

--- class Interpretator
       source = []
       setSourse(source)

       getHTML()
-------------------------------------------------------------------------------------------------------------------- """

from abstract_builder import blocks
from abstract_builder import loger

from collections import deque


class Fragment:
    tag = ""       # тег
    det = ""       # определитель тега
    spc = ""       # спецификатор тега

    level = ""     # уровень вложенности тега

    content = ""   # контент строки

    is_closed = False  # является ли данный фрагмент закрывающим для текущего блока (исп. при построении HTML-документа)
    is_opened = False  # является ли данный фрагмент открывающим для текущего блока (исп. при построении HTML-документа)

    def __str__(self):
        if self.is_closed:
            return "__<!CLOSED>__"
        elif self.is_opened:
            return "__<OPENED!>--"

        else:
            return f"({self.tag}) {self.content}"


class HtmlHelper:

    # построение строки HTML
    @staticmethod
    def makeStringHtml(not_ready_string):
        tag = blocks.getTag(det=not_ready_string.det)
        class_name = blocks.getClassName(det=not_ready_string.det, spc=not_ready_string.spc)
        content = not_ready_string.content

        if tag == "a":
            return "<{0} class=\"{1}\" href=\"{2}\"> {3} </{0}>\n".format(tag, class_name, content, content)

        return "<{0} class=\"{1}\"> {2} </{0}>\n".format(tag, class_name, content)

    # построение блока HTML
    @staticmethod
    def makeBlockHtml(head_element, content):
        # head_element - тег, на основе которого строится блок и который является заголовком этого блока

        tag_block = blocks.getTag(det=head_element.det, is_block=True)
        class_name = blocks.getClassName(det=head_element.det, spc=head_element.spc, is_block=True)
        header = HtmlHelper.makeStringHtml(head_element)

        if tag_block == "ul":
            header = ""

        return "<{0} class=\"{1}\">\n {2} {3} </{0}>\n".format(tag_block, class_name, header, content)


class InterpretatorHelper:

    """ содержит методы для упрощения реализации работы класса Interpretator """

    @staticmethod
    # разбиение строки на кортеж: тег и контент
    def parseLine(line):
        tag = ""
        content = ""

        first_space = line.find(" ")

        if first_space != -1:
            tag = line[:first_space]
            content = line[first_space + 1:]

        if tag == "":
            tag = None

        if content == "":
            content = None

        return tag, content

    # разбиение тега на кортеж: определитель и спецификатор
    @staticmethod
    def parseTag(tag):
        det = tag[0]
        spc = tag[1:]

        return det, spc


class Interpretator:

    # строки файла
    lines = []

    # подготовленные данные, для построения HTML-документа
    body = []  # основное содержимое
    meta = []  # мета-информация

    def __init__(self):
        lines = []
        body = []
        meta = []

    # получение источника строк
    def setSourse(self, source):
        self.lines = source
        self.lines.insert(1, blocks.ROOT_DET + "   ")

    # построение списков тегов для meta и body
    def buildingData(self):

        self.body = []
        self.meta = []

        loger.Loger.log_str(module_name="interpretator",
                            location="buildingData",
                            text="начало обработки строк файла")

        # флаг нужен для того, чтобы данные считывались толкьо внутри тегов '/*' и '*/'
        is_open = False

        for line in self.lines:

            line = line.replace("\n", "")

            if line.find("/*") == 0:
                is_open = True

            if is_open:

                if line == "*/":
                    is_open = False
                    break

                # ---- парсинг строки на тег и контент
                line_tuple = InterpretatorHelper.parseLine(line)

                tag = line_tuple[0]
                content = line_tuple[1]

                # строка line не соответствует формату
                if tag is None or content is None:
                    continue

                # ---- парсинг тега на опредлитель и спецификатор
                tag_tuple = InterpretatorHelper.parseTag(tag)

                det = tag_tuple[0]
                spc = tag_tuple[1]

                # это для того, чтобы заголовок списка не получал тег li
                if det == ">" and spc != "":
                    tag = "p"

                # строка line не соответствует формату
                if det is None or spc is None:
                    continue

                # создание объекта класса Fragment
                fragment = Fragment()

                fragment.tag = tag
                fragment.det = det
                fragment.spc = spc

                fragment.content = content

                # ---- определение принадлежности нового объекта Fragment к meta или body
                if fragment.det != blocks.META_DET:
                    self.body.append(fragment)
                else:
                    self.meta.append(fragment)

            # обнаружен закрывающий тег
            else:
                if line.find("*/") == 0:
                    is_open = False

        #  вывод body в файл для проверки
        #  file = open("log_buildingdata.txt", "w", encoding="utf-8")
        #
        #  for fragment in self.body:
        #      file.write(fragment.tag + " | " + fragment.content + "\n")

    # подготовка данных meta и body
    def prepareDate(self):

        loger.Loger.log_str(module_name="interpretator",
                            location="prepareDate",
                            text="подготовка данных meta и body")

        # ------ body
        levels_stack = deque()

        opened_fragment = Fragment()
        opened_fragment.is_opened = True

        closed_fragment = Fragment()
        closed_fragment.is_closed = True

        post_body = []  # обработанный список body

        for fragment in self.body:

            # ---- определение уровня вложенности тега фрагмента
            det_level = blocks.det_level.get(fragment.det)
            spc_level = blocks.spc_level.get(fragment.spc)

            if det_level is None:
                det_level = 0

            if spc_level is None:
                spc_level = 0

            fragment.level = det_level + spc_level

            if fragment.tag == "~?":
                fragment.level = blocks.LEVEL_TEXT

            # ---- вставка закрывающих фрагментов
            # WARNING: костыль, переменная равна True, если fragment - это пояснение к команде CLI
            is_command_comment = False

            if fragment.tag == "~?":
                post_body.append(fragment)
                is_command_comment = True

            while len(levels_stack) != 0:
                last_level = levels_stack[-1]

                if fragment.level >= last_level:
                    post_body.append(closed_fragment)
                    levels_stack.pop()
                else:
                    break

            # ---- запоминаем уровень рассматриваемого фрагмента, если он не текстовый
            if blocks.getTypeFragmentByLevel(fragment.level) is not blocks.FragmentType.TEXT:
                # с этого фрагмента начинается новый блок
                post_body.append(opened_fragment)
                levels_stack.append(fragment.level)

            # ---- завершение обработки рассматриваемого фрагмента
            if is_command_comment is False:
                post_body.append(fragment)

        # в конце файла ставится закрывающих фрагмент
        post_body.append(closed_fragment)

        self.body = post_body

    # формирование HTML для body
    def makeHtmlBody(self, index, head_fragment):

        html = ""

        while index < len(self.body):

            # открывающий фрагмент
            if self.body[index].is_opened:
                rec_tup = self.makeHtmlBody(index + 2, self.body[index + 1])

                index = rec_tup[0]
                html += rec_tup[1]

            # закрывающий фрагмент
            elif self.body[index].is_closed:
                html = HtmlHelper.makeBlockHtml(head_element=head_fragment, content=html)

                return index + 1, html

            elif blocks.getTypeFragmentByLevel(self.body[index].level) == blocks.FragmentType.TEXT:
                html += HtmlHelper.makeStringHtml(not_ready_string=self.body[index])
                index += 1

        return index, html

    # формирование HTML документа
    def getHtml(self):

        loger.Loger.log_str(module_name="interpretator",
                            location="getHtml",
                            text="создание HTML-разметки страницы")

        self.buildingData()
        self.prepareDate()

        """#  для отладки функции self.prepareDate()
        file = open("log_gethtml.txt", "w", encoding="utf-8")

        for fragment in self.body:
            file.write(fragment.__str__() + "\n")

        file.close()"""

        title = self.meta[0].content

        body_html = self.makeHtmlBody(index=2, head_fragment=self.body[1])[1]

        html = \
        "<!doctype html>" + \
        "<html lang=\"en\">" + \
        "<head>" + \
            "<meta charset=\"UTF-8\">" + \
            "<meta name=\"viewport\"" + \
            "content=\"width=device-width, user-scalable=no, initial-scale=1.0," + \
            "maximum-scale=1.0, minimum-scale=1.0\">" + \
            "<meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\">" + \
            "<title>" + title + "</title>" + \
            "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\">" + \
            "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">" + \
            "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>" + \
            "<link href=\"https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;700&display=swap\"" + \
            "rel =\"stylesheet\">" + \
            "<link rel=\"stylesheet\" href=\"static\style.css\">" +\
        "</head>" + \
        "<body>"

        html += \
        "<header class =\"header\" >" + \
            "<div class=\"header__inner\">" + \
                "<h1 class=\"header__pagename\">" + title + "</h1>" + \
            "</div>" + \
        "</header>"

        html += "<div class=\"content\">"

        html += body_html

        html += "<script src=\"static\main.js\"></script></div></body>"

        return html
