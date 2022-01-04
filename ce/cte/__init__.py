import re
import unicodedata
from uuid import UUID
from decimal import Decimal
from antlr4 import CommonTokenStream
from antlr4.InputStream import InputStream
from ce.cte.antlrgen.CTE import CTE as CTEParser
from ce.cte.antlrgen.CTEVisitor import CTEVisitor
from ce.cte.antlrgen.CTELexer import CTELexer
from ce.primitive_types import validated_string, validated_float
from ce.complex_types import Rid, Time, Timestamp
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

        return validated_string(
            ctx.STRING().getText().strip('"'),
            allow_NULs=self.config.get("allow_NULs", False),
        )

    def visitValueInt(self, ctx):
        if ctx.PINT_DEC() or ctx.NINT_DEC():
            return int(ctx.getText().replace("_", ""))

        if ctx.PINT_BIN():
            return int(ctx.PINT_BIN().getText().lstrip("0b").replace("_", ""), 2)

        if ctx.NINT_BIN():
            return -int(ctx.NINT_BIN().getText().lstrip("-0b").replace("_", ""), 2)

        if ctx.PINT_OCT():
            return int(ctx.PINT_OCT().getText().lstrip("0o").replace("_", "."), 8)

        if ctx.NINT_OCT():
            return -int(ctx.NINT_OCT().getText().lstrip("-0o").replace("_", "."), 8)

        if ctx.PINT_HEX():
            return int(ctx.PINT_HEX().getText().lstrip("0x").replace("_", "."), 16)

        if ctx.NINT_HEX():
            return -int(ctx.NINT_HEX().getText().lstrip("-0x").replace("_", "."), 16)

    def visitValueFloat(self, ctx):

        if ctx.FLOAT_DEC():
            return validated_float(ctx.FLOAT_DEC().getText())

        if ctx.FLOAT_HEX():
            return validated_float(ctx.FLOAT_HEX().getText(), as_hex=True)

        if ctx.INF():
            return float(ctx.INF().getText())

        if ctx.NAN():
            return Decimal("nan")

        if ctx.SNAN():
            return Decimal("snan")

    def visitValueUid(self, ctx):
        return UUID(ctx.UID().getText())

    def visitValueRid(self, ctx):
        text = ctx.RID().getText()
        return Rid(text, allow_NULs=self.config.get("allow_NULs", False))

    def visitValueTime(self, ctx):

        if ctx.TIME():
            return Time.from_string(ctx.TIME().getText())

        if ctx.DATE():
            return Timestamp.from_string(ctx.DATE().getText())

    def visitContainerList(self, ctx):
        return [self.visit(context) for context in ctx.value()]


def dump():
    pass


def load(text: str):
    lexed_text = CTELexer(InputStream(text))
    lexed_text.removeErrorListeners()
    parsed_text = CTEParser(CommonTokenStream(lexed_text))
    parsed_text._errHandler = BailErrorStrategy()
    return __TextToObject().visit(parsed_text.cte())
