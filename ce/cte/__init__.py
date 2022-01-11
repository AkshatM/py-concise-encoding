import re
import unicodedata
from uuid import UUID
from decimal import Decimal
from antlr4 import CommonTokenStream
from antlr4.InputStream import InputStream
from ce.cte.antlrgen.CTE import CTE as CTEParser
from ce.cte.antlrgen.CTEVisitor import CTEVisitor
from ce.cte.antlrgen.CTELexer import CTELexer
from ce.primitive_types import read_string, read_int, read_float
from ce.complex_types import Rid, Time, Timestamp
from ce.container_types import Map, Value
from antlr4.error.ErrorStrategy import BailErrorStrategy


class __TextToObject(CTEVisitor):
    """
    Cast a tokenized CTE stream into a Python dictionary.
    """

    def __init__(self, config={}):
        self.state = None
        self.config = config

    def visitCte(self, ctx):

        self.state = self.visit(ctx.value())
        return self.state

    def visitValueNull(self, ctx):
        return None

    def visitValueBool(self, ctx):
        if ctx.TRUE():
            return True

        if ctx.FALSE():
            return False

    def visitValueString(self, ctx):

        return read_string(
            ctx.STRING().getText().strip('"'),
            allow_NULs=self.config.get("allow_NULs", False),
        )

    def visitValueInt(self, ctx):
        return read_int(ctx.getText())

    def visitValueFloat(self, ctx):
        return read_float(ctx.getText())

    def visitValueUid(self, ctx):
        return UUID(ctx.UID().getText())

    def visitValueRid(self, ctx):
        text = ctx.RID().getText().rstrip('"').lstrip('@"')
        return Rid(text, allow_NULs=self.config.get("allow_NULs", False))

    def visitValueTime(self, ctx):

        if ctx.TIME():
            return Time.from_string(ctx.TIME().getText())

        if ctx.DATE():
            return Timestamp.from_string(ctx.DATE().getText())

    def visitContainerList(self, ctx):
        return [self.visit(context) for context in ctx.value()]

    def visitKvPair(self, ctx):
        return (self.visit(v) for v in ctx.value())

    def visitContainerMap(self, ctx):
        return Map((self.visit(pair) for pair in ctx.kvPair()))


def dump(value: Value):

    stringified_value = "null"
    
    match value:
        case int():
            stringified_value = str(value)
        case _:
            raise Exception("Not implemented")

    return f"c1 {stringified_value}"


def load(text: str):
    lexed_text = CTELexer(InputStream(text))
    lexed_text.removeErrorListeners()
    parsed_text = CTEParser(CommonTokenStream(lexed_text))
    parsed_text._errHandler = BailErrorStrategy()
    return __TextToObject().visit(parsed_text.cte())
