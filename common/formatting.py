import re


def escape_symbols(s):
    s = re.escape(s)
    s = re.sub(r'\!', '\!', s)
    s = re.sub(r'\=', '\=', s)
    s = re.sub(r'\`', '\`', s)
    s = re.sub(r'\<', '\<', s)
    s = re.sub(r'\>', '\>', s)
    s = re.sub(r'\+', '\+', s)
    return s


def escape_headers(s, open_symbol="*", close_symbol="*"):
    # Заменяем заголовки
    pattern = re.compile(r'^(#{2,6})\s+(.*)', re.MULTILINE)
    return re.sub(pattern, lambda match: f"{open_symbol}{match.group(2)}{close_symbol}", s)


def escape_markdown_symbols(s):
    s = escape_headers(s)
    characters_to_escape = set("!@#$%^&+-={}\\./|<>()[]")
    escaped_string = ''.join(['\\' + char if char in characters_to_escape else char for char in s])
    return escaped_string


def markdown_to_html(s):
    # Сначала заменяем **жирный** текст
    s = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", s)
    # Затем заменяем *курсивный* текст
    s = re.sub(r"\*(.*?)\*", r"<i>\1</i>", s)

    # Заменяем заголовки
    s = escape_headers(s, "<b>", "</b>")

    return s
