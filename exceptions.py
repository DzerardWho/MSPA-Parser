class ParsingException(Exception):
    '''
    Base exception class
    '''

    def __init__(self, pos, srcText):
        self.message = ''
        lines = srcText.splitlines()
        for lineNr in range(len(lines)):
            line = lines[lineNr]
            lineLen = len(line)

            if (pos - lineLen) < 0:
                self.line = line + '\n' + (' ' * pos) + '^'
                self.lineNr = lineNr
                break
            else:
                pos -= lineLen + 1

    def __str__(self):
        return self.message


class MissingArgument(ParsingException):
    def __init__(self, pos, srcText):
        super().__init__(pos, srcText)
        self.message = f'Błąd w lini {self.lineNr}: Wymagane jest podanie \
argumentu.\n{"*" * 10}\n{self.line}\n{"*" * 10}'


class NoText(ParsingException):
    def __init__(self, pos, srcText):
        super().__init__(pos, srcText)
        self.message = f'Błąd w lini {self.lineNr}: Brak tekstu.\
\n{"*" * 10}\n{self.line}\n{"*" * 10}'


class ParameterConflict(ParsingException):
    def __init__(self, pos, srcText, params):
        super().__init__(pos, srcText)
        self.message = f'Błąd w lini {self.lineNr}: Konflikt parametrów \
"{params[0]}" i "{params[1]}".\n{"*" * 10}\n{self.line}\n{"*" * 10}'


class UnexpectedParameter(ParsingException):
    def __init__(self, pos, srcText, param):
        super().__init__(pos, srcText)
        self.message = f'Błąd w lini {self.lineNr}: Parametr "{param}" nie \
może występować z innymi parametrami.\n{"*" * 10}\n{self.line}\n{"*" * 10}'


class DuplicatedParameter(ParsingException):
    def __init__(self, pos, srcText, param):
        super().__init__(pos, srcText)
        self.message = f'Błąd w lini {self.lineNr}: Parametr "{param}" \
występuje wielokrotnie w jednym tagu.\n{"*" * 10}\n{self.line}\n{"*" * 10}'
