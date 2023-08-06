""" --------------------------------------------------------------------------------------------------------------------
Cодержит информацию о тегах, определителях и спецификаторах, названиях классов, а так же других данных, для формирования
HTML-документа, и функции для получения готовых данных

--- META_DET
--- ROOT_DET

--- LEVEL_HEADINHG
--- LEVEL_TEXT
--- LEVEL_OTHER

--- det_level
--- spc_level

--- class FragmentType
--- getTypeFragmentByLevel(level)

--- det_classes
--- det_classes_blocks
--- spc_classes

--- det_tags
--- det_tags_blocks

--- getClassName(det, spc)
--- getTag(det)

-------------------------------------------------------------------------------------------------------------------- """


META_DET = "%"  # определитель, используемый для отображении мета-информации
ROOT_DET = "@"  # определитель корневого элемента


# ------------------------------------------- УРОВНИ ВЛОЖЕННОСТИ
LEVEL_HEADINHG = 1000000
LEVEL_TEXT     = 10000
LEVEL_OTHER    = 100

# уровень вложенности определителей
det_level = {
    # корневой элемент
    ROOT_DET:    LEVEL_HEADINHG * 2,

    # заголовки
    "*":    LEVEL_HEADINHG,

    # обычный текст
    "?":    LEVEL_TEXT,
    "&":    LEVEL_TEXT,
    "!":    LEVEL_TEXT,
    "t":    LEVEL_TEXT,
    "$":    LEVEL_TEXT,

    # другие
    ">":    100,
    "~":    102,
}

# уровень вложенности спецификаторов
spc_level = {
    "----":  4,
    "--":    2,
    "":      0,
}


# определение типа фрагмента (заголовок, обычный текст и т.д.) по урвоню
class FragmentType:
    HEADING = 3,
    TEXT    = 2,
    OTHER   = 1,
    NONE    = 0


def getTypeFragmentByLevel(level):
    if level >= LEVEL_HEADINHG:
        return FragmentType.HEADING
    elif level >= LEVEL_TEXT:
        return FragmentType.TEXT
    elif level >= LEVEL_OTHER:
        return FragmentType.OTHER

    else:
        return FragmentType.NONE


# ------------------------------------------- НАЗВАНИЯ КЛАССОВ
# название классов элементов с содержимым по определителям
det_classes = {
    ROOT_DET:    "content",
    "*":    "title",
    "?":    "paragraph",
    "!":    "critical",
    "t":    "todo",
    "$":    "mark",
    ">":    "item",
    "&":    "link",
    "~":    "command",
}


# названия классов блоков
det_classes_blocks = {
    "*":    "block",
    "~":    "command__block",
    ">":    "list",
}

# спецификаторы классов
spc_classes = {
    "----": "-4",
    "--":   "-2",
    "?":    "__comment",
    "":     "",
    "odo":  "",
}


# ------------------------------------------- НАЗВАНИЯ ТЕГОВ
# теги элементов с содержимым по определителям
det_tags = {
    ROOT_DET:    "div",
    "*":    "p",
    "?":    "p",
    "!":    "p",
    "t":    "p",
    "$":    "p",
    ">":    "li",
    "&":    "a",
    "~":    "p",
}

# теги блоков
det_tags_blocks = {
    "*":    "div",
    "~":    "div",
    ">":    "div",
}


# ------------------------------------------- ФУНКЦИИ ДЛЯ ФОРМИРОВАНИЯ ДАННЫХ ПО ТЕГАМ
# формирование имени класса по определителю и спецификатору
def getClassName(det, spc, is_block=False):
    _det = None

    if is_block is False:
        _det = det_classes.get(det)
    else:
        _det = det_classes_blocks.get(det)

    _spc = spc_classes.get(spc)

    if _det is not None and _spc is not None:
        return _det + _spc

    return None


# формирование тега по определителю
def getTag(det, is_block=False):
    _det = None

    if is_block is False:
        _det = det_tags.get(det)
    else:
        _det = det_tags_blocks.get(det)

    if _det is not None:
        return _det

    return None
