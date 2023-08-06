class InvalidDeclaration:
    label = "Invalid declaration inside record when field() was expected"


class OpeningBraceExpected:
    label = "'{' expected"


class ClosingBraceExpected:
    label = "'}' expected"


class ClosingQuoteExpected:
    label = "'\"' expected"


class TooManyArguments:
    label = "Too many arguments"


class TooFewArguments:
    label = "Too few arguments"


class InvalidRecordType:
    label = "Invalid record type"


DB_ERROR = {
    TooManyArguments: [
        'record(ai, "bar", foo)',
        'record(ai, "bar") {\n field(foo, "bar", bar)\n }',
        'record(ai, "bar") {\n field(foo, bar, bar)\n }',
        'record(ai, "bar") {\n field(foo, bar, "bar")\n }',
        'record(ai, "bar") {\n field(foo, "bar", "bar")\n }',
    ],
    ClosingQuoteExpected: [
        'record(ai, "bar) {\n field(DESC, "bar")\n}',
        'record(ai, "bar) {\n bar \n}',
        'record(ai, "bar") {\n field(DESC, "bar)\n}',
        'record(ai, "bar") {\n field(DESC, "bar")\n field(DESC, "bar)\n}',
    ],
    TooFewArguments: ["record(ai)", "record(ai,)"],
    InvalidRecordType: ['record(foo, "bar")'],
    InvalidDeclaration: [
        'record(ai, "foo) {\nfoo(bar, "bar")}',
        'record(ai, "bar") {\n bar }',
        'record(ai, "bar") {\n field(DESC, "bar")\n foo(EVNT, "aaa")\n}',
    ],
    OpeningBraceExpected: [
        'record(ai, "bar") \nfield(DESC, "bar")\n}',
        'record(ai, bar) \nfield(DESC, "bar")\n}',
    ],
    ClosingBraceExpected: [
        'record(ai, "bar") {\n field(DESC, "bar") \nrecord(foo, "bar")',
        'record(ai, "bar") {\n field(DESC, "bar") \nfield(DTYP, "stream") \nrecord(foo, "bar")',
        'record(ai, "a) {\n field(foo, bar)',
        'record(ai, "a") {\n field(foo, bar)',
        'record(ai, "bar") {\n field(DESC, "bar")\n field(EVNT, "aaa")}',
    ],
}

DESC_TOO_LONG = "Record description too long (maximum of 40)"
REC_TOO_LONG = "Record name too long (maximum of 60)"
