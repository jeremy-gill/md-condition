from __future__ import unicode_literals, absolute_import
import re

from markdown.preprocessors import Preprocessor


class ConditionPreprocessor(Preprocessor):

    RE_START = re.compile(r'[ \t]*<!--- #if (.*) -->')
    RE_END = re.compile(r'[ \t]*<!--- #endif -->')
    RE_ELSE = re.compile(r'[ \t]*<!--- #else -->')

    def __init__(self, md, extension):
        super(ConditionPreprocessor, self).__init__(md)
        symbol = extension.getConfig('symbol')
        if isinstance(symbol, str):
            symbol = [symbol,]
        self.symbols = symbol

    def run(self, lines):
        new_lines = []

        matching_stack = []
        symbol_matching_stack = []
        start_head_stack = []

        matching = False
        symbol_matching = False
        for line in lines:
            start_head = False
            if self.RE_START.match(line):
                start_head_stack.append(start_head)
                start_head = True
                matching_stack.append(matching)
                matching = True
                sym = self.RE_START.split(line)[1]
                symbol_match_start = (sym in self.symbols)
                symbol_matching_stack.append(symbol_matching)
                if symbol_match_start:
                    symbol_matching = True
                else:
                    symbol_matching = False
                continue
            if self.RE_ELSE.match(line):
                symbol_matching = not symbol_matching
                continue
            if self.RE_END.match(line):
                matching = matching_stack.pop()
                if len(symbol_matching_stack) > 0:
                    symbol_matching = symbol_matching_stack.pop()
                else:
                    symbol_matching = False
                continue
            if not matching or (symbol_matching and False not in symbol_matching_stack[1:])and not start_head:
                new_lines.append(line)
        return new_lines