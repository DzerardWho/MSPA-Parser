from arpeggio import ParserPython, visit_parse_tree
from .parserRules import mspaText
from .treeVisitor import Visitor


def parse(text):
    parser = ParserPython(
        mspaText,
        debug=False,
        reduce_tree=False,
        skipws=False,
        ws="\t ",
        memoization=True
    )

    return parser.parse(text)


def generateDict(text):
    return visit_parse_tree(parse(text), Visitor(src=text))
