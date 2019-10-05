import arpeggio as ar
from arpeggio import RegExMatch as _


def newLine():
    return ar.ZeroOrMore(_(r'\n|\r'))


def space():
    return ' '


def option():
    return ar.ZeroOrMore(space), _(r'\w+'), ar.ZeroOrMore(space), 


def tagOptions():
    # return ar.Sequence(option, ar.ZeroOrMore(',', option, skipw=True), skipw=True)
    return ar.OneOrMore(option, sep=",", skipw=True)


def beginTag():
    return _(r'(?<!\\|/)<')


def endTag():
    return _(r'(?<!\\|/)>')


def tag():
    return beginTag, tagOptions, ':', ar.Optional(inTagText), endTag


def normalText():
    return _(r'(((?:\\|/)<)|([^<]))+')
    # return ar.ZeroOrMore(ar.Not(endTag), _(r'.'))


def inTagNormalText():
    return _(r'(((?:\\|/)(?:<|>))|([^<>]))+')


def inTagText():
    return ar.OneOrMore([tag, ar.Optional(inTagNormalText)])


def text():
    return [tag, ar.Optional(normalText)]


def mspaText():
    return ar.ZeroOrMore(text), ar.EOF


if __name__ == "__main__":
    parser = ar.ParserPython(mspaText, debug=True, skipws=False)
