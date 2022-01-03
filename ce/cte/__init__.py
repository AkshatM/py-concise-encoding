import re
import unicodedata
from uuid import UUID
from decimal import Decimal
from antlr4 import CommonTokenStream
from antlr4.InputStream import InputStream
from ce.cte.antlrgen.CTE import CTE as CTEParser
from ce.cte.antlrgen.CTEVisitor import CTEVisitor
from ce.cte.antlrgen.CTELexer import CTELexer
from ce.cte.utils import validate_string, validate_float, validate_time
from antlr4.error.ErrorStrategy import BailErrorStrategy


class __TextToObject(CTEVisitor):
    """
    Cast a tokenized CTE stream into a Python dictionary.
    """

    def __init__(self):
        self.state = None

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

        # In Python, floats smaller than the IEE-754 range get silently cast
        # to 0.0. This is a violation of the CE spec, which requires a data
        # error in such cases. Hence, we artificially detect it for FLOAT_DEC/HEX
        # by checking if the text "looks like" a pattern that should not have been
        # cast to zero but was, which is doable because there are only finitely
        # many such patterns.

        # Python will also sometimes cast an out-of-range large float value to "inf", so we
        # explicitly disallow that case.

        if ctx.FLOAT_DEC():

            # The following zero_pattern matches -0.0,00.000,0.000, 0.0e0, 0.0e20 etc.
            # and disallows 0.1, etc. The one case it fails on is 0.e0, but this is
            # fine because Antlr will reject it at this stage.
            zero_pattern = r"^-?0+(?P<dot>\.)?(?(dot)0+)(?P<exp>e)?(?(exp).*)$"

            return validate_float(ctx.FLOAT_DEC().getText(), zero_pattern)

        if ctx.FLOAT_HEX():

            # The following zero_pattern matches -0x0p0, 0x0000p+0, 0x0000p-0, 0x0.0p-0 etc.
            zero_pattern = r"^-?0x0+(?P<dot>\.)?(?(dot)0+)(?P<exp>p)?(?(exp).*)$"
            return validate_float(ctx.FLOAT_HEX().getText(), zero_pattern, as_hex=True)

        if ctx.INF():
            return float(ctx.INF().getText())

        if ctx.NAN():
            return Decimal("nan")

        if ctx.SNAN():
            return Decimal("snan")

    def visitValueUid(self, ctx):
        return UUID(ctx.UID().getText())

    def visitValueRid(self, ctx):
        text = ctx.RID().getText().rstrip('"').lstrip('@"')
        return validate_string(text)

    def visitValueTime(self, ctx):

        if ctx.TIME():
            return validate_time(ctx.TIME().getText())


def dump():
    pass


def load(text: str):
    lexed_text = CTELexer(InputStream(text))
    lexed_text.removeErrorListeners()
    parsed_text = CTEParser(CommonTokenStream(lexed_text))
    parsed_text._errHandler = BailErrorStrategy()
    return __TextToObject().visit(parsed_text.cte())
