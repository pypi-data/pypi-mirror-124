import sys
from   tokenize import tokenize, untokenize

from violence.utils import puts, raw_input

ставить = puts

продвинутое_получение = raw_input
продвинутый_ввод      = raw_input

вывести    = print
консоль    = print
напечатать = print

перебрать = range
получить  = input
ввод      = input

тип       = type
число     = int
строка    = str
истина    = bool
плавающее = float

лист    = list
кортеж  = tuple
сбор    = set
словарь = dict

округлить = round
открыть   = open

хэш  = hash
айди = id
хекс = hex
хэкс = hex

выйти = quit
выход = quit 

swap = {
    'для':  'for',
    'в':    'in',
    'пока': "while",
    "с":    "with",
    "как":  "as",
    "это":  "is",

    "глобал":     "global",
    "глобально":  "global",
    "глобальный": "global",

    "завершить":  "break",
    "продолжить": "continue",

    "функция": "def",
    
    'удалить': 'del',
    
    "асинхронная": "async",
    "асинхронно":  "async",

    "асинх": "await",
    "асинк": "await",
    
    "вернуть": "return",
    
    "попытаться": "try",
    "попытка":    "try",
    "исключая":   "except",
    
    "Истина":  "True",
    "Правда":  "True",
    "Внатуре": "True",
    "Ложь":    "False",
    "Пиздешь": "False",
    
    "если":  "if",
    "аесли": "elif",
    "или":   "elif",
    "иначе": "else",

    "Исключение": "Exception",
    
    "класс":      "class",
    "любое":      "any",
    "все":        "all",
    "или":        "or",
    "и":          "and",
    "ничего":     "None",
    "оставить":   "pass",
    "пропустить": "pass",

    "свойство":    "property",
    "имущество":   "property",
    "статическая": "staticmethod",
    "статически":  "staticmethod",
    "классовая":   "classmethod",
    "классово":   "classmethod",

    "свой": "self",
    "своя": "self",
    "свои": "self",
    "свое": "self",
    "своё": "self",

    "__задать__": "__init__",
    "__строка__": "__str__",

    "импортировать": "import",
    "загрузить":     "import",
    "из":            "from",

    "разбить":  "split",
    "обрезать": "strip",

    "добавить": "append",
    "индекс": "index",
    "удалить": "remove",
    "выбросить": "pop",
    "очистить": "clear",
    "копировать": "copy",
    "развернуть": "reverse",
    "сортировать": "sort",

    "вызвать": "raise",

    "экземпляр": "isinstance",

    "закрыть": "close",
    "записать": "write",
    "читать": "read",
    "прочитать": "read",
    "прочестьлинии": "readlines",
    "прочитатьлинии": "readlines",
    "прочестьлинию": "readline",
    "прочитатьлинию": "readline",
    "искать": "seek",

    "кодировка": "encoding",

    "предметы": "items",
    "значения": "values",
    "ключи": "keys",
}

def __unrupy__():
    try:
        filename = sys.argv[1]
    except:
        return

    with open(filename, 'rb') as src:
        tokens = []
        
        for token in tokenize(src.readline):
            if token.type == 1 and token.string in swap:
                tokens.append((token.type, swap[token.string]))
            else:
                tokens.append((token.type, token.string))

    code = untokenize(tokens).decode('utf-8') 

    with open(f"{filename.split('.py')[0]}-original.py", "a+", encoding = "utf8") as file:
        file.write(code)

def __main__():
    try:
        filename = sys.argv[1]
    except:
        return

    with open(filename, 'rb') as src:
        tokens = []
        
        for token in tokenize(src.readline):
            if token.type == 1 and token.string in swap:
                tokens.append((token.type, swap[token.string]))
            else:
                tokens.append((token.type, token.string))

    code = untokenize(tokens).decode('utf-8') 

    exec(code)

if __name__ == "__main__":
    __main__()
