from lark.exceptions import UnexpectedToken
from lark.lexer import Token
from epics_linter.common import print_error
from epics_linter.db import (
    DESC_TOO_LONG,
    REC_TOO_LONG,
    ClosingBraceExpected,
    ClosingQuoteExpected,
    InvalidDeclaration,
    InvalidRecordType,
    OpeningBraceExpected,
    TooFewArguments,
    DB_ERROR as DB_EX,
    TooManyArguments,
)
from lark import Lark
from pathlib import Path


class Linter:
    def __init__(self):
        grammar_path = Path(__file__).parent

        self.parser = Lark.open(
            grammar_path / "grammars/db.lark",
            rel_to=__file__,
            parser="lalr",
            propagate_positions=True,
        )

        self.grammar_error = False

    def lint(self, input):
        self.grammar_error = False
        try:
            parsed = self.parser.parse(input, on_error=self.parse_error)
            if self.grammar_error:
                return

            for record in parsed.children:
                record = record.children
                if len(record[1]) > 60:
                    print_error(REC_TOO_LONG, record[1])
                    continue
                for field in record[2:]:
                    if field.children[0] == "DESC" and len(field.children[1]) > 40:
                        print_error(DESC_TOO_LONG, field.children[1])

        except UnexpectedToken as e:
            if not e.token.type == "$END":
                raise ValueError
        except AttributeError:
            return

    def parse_error(self, e):
        err = e.match_examples(self.parser.parse, DB_EX)
        if not err:
            return True

        ignore = False

        if err is TooFewArguments:
            if e.token.type == "COMMA":
                e.interactive_parser.feed_token(Token("ESCAPED_STRING", ""))
            else:
                e.interactive_parser.feed_token(Token("COMMA", ","))
                e.interactive_parser.feed_token(Token("ESCAPED_STRING", ""))
        if err is InvalidRecordType:
            e.interactive_parser.feed_token(Token("RECORD_TYPE", ""))
        if err is ClosingBraceExpected:
            if "NEWLINE" in e.accepts:
                e.interactive_parser.feed_token(Token("NEWLINE", "\n"))
            e.interactive_parser.feed_token(Token("RBRACE", "}"))
        if err is OpeningBraceExpected:
            e.interactive_parser.feed_token(Token("LBRACE", "{"))
        if err is TooManyArguments:
            if e.token.type == "COMMA":
                ignore = True
        if err is ClosingQuoteExpected:
            e.interactive_parser.feed_token(Token("WORD", ""))
        if err is InvalidDeclaration:
            e.interactive_parser.feed_token(Token("_FIELD_HEAD", "field("))
        if not ignore:
            print_error(err.label, e)
            self.grammar_error = True

        return True
