from konlpy.tag import Mecab, Kkma, Komoran

mecab = Mecab()
kkma = Kkma()
komo = Komoran()


def konlpy_filter(text):
    text = text.upper()

    noun_list = list(
        set([*mecab.nouns(text), *kkma.nouns(text), *komo.nouns(text)]))

    return noun_list
