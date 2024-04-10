languages = [
    {'English 🇺🇸': {
        'start': '👋 █▓▒▒░░░ Welcome to our bot! ░░░▒▒▓█',
    }},
    {'Pусский 🇷🇺': {
        'start': '👋 █▓▒▒░░░ добро пожаловать к нашему боту! ░░░▒▒▓█',
    }}
]

LANGS = ["English 🇺🇸", "Pусский 🇷🇺"]


def find_language(locale):
    for idx, lang in enumerate(LANGS):
        if lang == locale:
            return idx
    return None
