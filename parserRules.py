import arpeggio as ar
from arpeggio import RegExMatch as _


def space():
    return ar.ZeroOrMore(_(r'\t| '))


def plainText():
    return ar.Optional(_(r'(((?:\\|/)(?:<|>))|([^<>]))+'))


def HTMLText():
    return ar.Optional(_(r'.*?(?:\/|\\)>'))


def beginTag():
    return _(r'(?<!\\|/)<')


def endTag():
    return _(r'(?<!\\|/)>')


def tag():
    return beginTag, tagOptions, ar.Optional(':', text), endTag


def defTag():
    return (beginTag, space, _(r'def', ignore_case=True),
            space, arg, ':', tagOptions, endTag)


def HTMLTag():
    return (beginTag, space, _(r'html', ignore_case=True), space,
            ':', HTMLText, _(r'(?:\\|/)>'))


def params():
    return _(r'img|quirk|url|id|style|html|def', ignore_case=True)


def paramsWithArgs():
    return params, space, arg


def classes():
    return _(r'#?\w+')


def arg():
    return ar.Optional(beginTag, plainText, endTag, space)


def keyWords():
    return [paramsWithArgs, classes]


def tagOptions():
    return ar.OneOrMore(space, keyWords, space, sep=",", skipw=True)


def text():
    return ar.ZeroOrMore([defTag, HTMLTag, tag, plainText])


def mspaText():
    return text, ar.EOF


if __name__ == "__main__":
    parser = ar.ParserPython(mspaText, debug=True, skipws=False)
