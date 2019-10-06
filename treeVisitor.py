import re

from arpeggio import PTNodeVisitor

from .exceptions import (DuplicatedParameter, MissingArgument, NoText,
                         ParameterConflict, UnexpectedParameter)


def checkConflict(value, params):
    if value is 'url':
        if 'img' in params:
            return ['url', 'img']
    elif value is 'img':
        if 'url' in params:
            return ['img', 'url']
    return None


class visitor(PTNodeVisitor):
    def __init__(self, *args, src, **kwargs):
        super().__init__(*args, **kwargs)
        self.src = src

    def visit_plainText(self, node, children):
        text = node.value

        text = re.sub('\\>|/>', '>;', text)
        text = re.sub('\\<|/<', '<;', text)

        # return text.split('\n')
        return text

    def visit_HTMLText(self, node, children):
        return node.value

    def visit_defTagText(self, node, children):
        text = node.value

        if len(text) == 0:
            raise NoText(node.position, self.src)

        text = re.sub('\\>|/>', '>;', text)
        text = re.sub('\\<|/<', '<;', text)

        return text

    def visit_tag(self, node, children):
        return {
            'type': 'tag',
            'settings': children.tagOptions[0],
            'text': children.text,
        }

    def visit_text(self, node, children):
        return list(children)

    def visit_defTag(self, node, children):
        arg = children.arg
        if len(arg) == 0 or (len(arg) == 1 and arg[0] == [None]):
            raise MissingArgument(node.position, self.src)

        return {
            'settings': {},
            'type': 'def',
            'name': children.arg[0],
            'content': children.defTagText,
        }

    def visit_HTMLTag(self, node, children):
        return {
            'settings': {},
            'type': 'html',
            'content': children.HTMLText,
        }

    def visit_macro(self, node, children):
        return node.value[1:]

    def visit_params(self, node, children):
        return node.value

    def visit_paramsWithArgs(self, node, children):
        param = children.params[0].lower()
        if param in ['html', 'def']:
            return {'settings': param, 'error': True, }

        arg = children.arg

        if len(arg) == 0 or (len(arg) == 1 and arg[0] == [None]):
            if param == 'quirk':
                arg = 0
            elif param in ['id', 'style']:
                arg = ''
            else:
                raise MissingArgument(node.position, self.src)
        else:
            arg = arg[0]

        return {
            'settings': param,
            'content': arg,
        }

    def visit_arg(self, node, children):
        value = children.plainText
        if len(value):
            return value[0]
        return [None]

    def visit_classes(self, node, children):
        return node.value

    def visit_keyWords(self, node, children):
        params = {}

        for key in children.paramsWithArgs:
            param = key['settings']
            if 'error' in key:
                raise UnexpectedParameter(node.position, self.src, param)
            if param in params:
                raise DuplicatedParameter(node.position, self.src, param)
            conflicts = checkConflict(param, params)
            if conflicts:
                raise ParameterConflict(node.position, self.src, conflicts)
            params[param] = key['content']

        return {
            'params': params,
            'classes': children.classes,
            'makros': children.makro,
        }

    def visit_tagOptions(self, node, children):
        return children.keyWords[0]
