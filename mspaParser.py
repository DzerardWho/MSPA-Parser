import arpeggio as ar
from arpeggio import RegExMatch as _


def newLine():
    return ar.ZeroOrMore(_(r'\n|\r'))


def space():
    return ar.ZeroOrMore(_(r'\t| '))


def arg():
    return ar.Optional(beginTag, ar.Optional(inTagNormalText), endTag, space)


def option():
    return space, _(r'\w+'), space, arg


def keyWords():
    return [paramsWithArgs, paramsClasses]


def tagOptions():
    # return ar.Sequence(option, ar.ZeroOrMore(',', option, skipw=True),
    #                    skipw=True)
    return ar.OneOrMore(space, keyWords, space, sep=",", skipw=True)


def beginTag():
    return _(r'(?<!\\|/)<')


def endTag():
    return _(r'(?<!\\|/)>')


def tag():
    return beginTag, tagOptions, ':', ar.Optional(inTagText), endTag


def paramsClasses():
    return _(r'\w+', ignore_case=True)


def paramsWithArgs():
    return _(r'img|quirk|url|def|id|style', ignore_case=True), space, arg


def HTMLText():
    return _(r'.*?(?:\/|\\)>')


def HTMLTag():
    return (beginTag, space, _(r'html', ignore_case=True), space, arg,
            ':', ar.Optional(HTMLText), _(r'(?:\\|/)>'))


def normalText():
    return _(r'(((?:\\|/)<)|([^<]))+')
    # return ar.ZeroOrMore(ar.Not(endTag), _(r'.'))


def inTagNormalText():
    return _(r'(((?:\\|/)(?:<|>))|([^<>]))+')


def inTagText():
    return ar.OneOrMore([HTMLTag, tag, ar.Optional(inTagNormalText)])


def text():
    return [HTMLTag, tag, ar.Optional(normalText)]


def mspaText():
    return ar.ZeroOrMore(text), ar.EOF


if __name__ == "__main__":
    parser = ar.ParserPython(mspaText, debug=True, skipws=False)
