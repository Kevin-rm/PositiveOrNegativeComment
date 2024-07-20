from googletrans import Translator
from langdetect import detect

translator = Translator()


def translate(text: str, source: str = "mg", destination: str = "en") -> str:
    global translator

    if not isinstance(text, str):
        raise TypeError("L'argument text n'est pas de type \"string\"")
    if not isinstance(translator, Translator):
        raise TypeError("L'argument translator n'est pas de type \"googletrans.client.Translator\"")

    if text is None or translator is None:
        raise ValueError("Tous les arguments ne doivent pas être \"null\"")
    if text.strip() == "":
        raise ValueError("L'argument text ne peut pas être vide")

    return translator.translate(text, src=source, dest=destination).text


def is_english(text: str) -> bool:
    if not isinstance(text, str):
        raise TypeError("L'argument text n'est pas de type \"string\"")

    try:
        return detect(text) == "en"
    except:
        return False
