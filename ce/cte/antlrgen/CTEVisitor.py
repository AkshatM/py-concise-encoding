# Generated from CTE.g4 by ANTLR 4.9.3
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .CTE import CTE
else:
    from CTE import CTE

# This class defines a complete generic visitor for a parse tree produced by CTE.


class CTEVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CTE#cte.
    def visitCte(self, ctx: CTE.CteContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#value.
    def visitValue(self, ctx: CTE.ValueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#version.
    def visitVersion(self, ctx: CTE.VersionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#valueNull.
    def visitValueNull(self, ctx: CTE.ValueNullContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#valueUid.
    def visitValueUid(self, ctx: CTE.ValueUidContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#valueBool.
    def visitValueBool(self, ctx: CTE.ValueBoolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#valueInt.
    def visitValueInt(self, ctx: CTE.ValueIntContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#valueFloat.
    def visitValueFloat(self, ctx: CTE.ValueFloatContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#valueTime.
    def visitValueTime(self, ctx: CTE.ValueTimeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#valueString.
    def visitValueString(self, ctx: CTE.ValueStringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#valueRid.
    def visitValueRid(self, ctx: CTE.ValueRidContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#customText.
    def visitCustomText(self, ctx: CTE.CustomTextContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#kvPair.
    def visitKvPair(self, ctx: CTE.KvPairContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#markerID.
    def visitMarkerID(self, ctx: CTE.MarkerIDContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#marker.
    def visitMarker(self, ctx: CTE.MarkerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#reference.
    def visitReference(self, ctx: CTE.ReferenceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#remoteRef.
    def visitRemoteRef(self, ctx: CTE.RemoteRefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#markupName.
    def visitMarkupName(self, ctx: CTE.MarkupNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#markupContents.
    def visitMarkupContents(self, ctx: CTE.MarkupContentsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#containerMap.
    def visitContainerMap(self, ctx: CTE.ContainerMapContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#containerList.
    def visitContainerList(self, ctx: CTE.ContainerListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#containerEdge.
    def visitContainerEdge(self, ctx: CTE.ContainerEdgeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#containerNode.
    def visitContainerNode(self, ctx: CTE.ContainerNodeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#containerMarkup.
    def visitContainerMarkup(self, ctx: CTE.ContainerMarkupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemBits.
    def visitArrayElemBits(self, ctx: CTE.ArrayElemBitsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemInt.
    def visitArrayElemInt(self, ctx: CTE.ArrayElemIntContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemIntB.
    def visitArrayElemIntB(self, ctx: CTE.ArrayElemIntBContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemIntO.
    def visitArrayElemIntO(self, ctx: CTE.ArrayElemIntOContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemIntX.
    def visitArrayElemIntX(self, ctx: CTE.ArrayElemIntXContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemUint.
    def visitArrayElemUint(self, ctx: CTE.ArrayElemUintContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemUintB.
    def visitArrayElemUintB(self, ctx: CTE.ArrayElemUintBContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemUintO.
    def visitArrayElemUintO(self, ctx: CTE.ArrayElemUintOContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemUintX.
    def visitArrayElemUintX(self, ctx: CTE.ArrayElemUintXContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemFloat.
    def visitArrayElemFloat(self, ctx: CTE.ArrayElemFloatContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemFloatX.
    def visitArrayElemFloatX(self, ctx: CTE.ArrayElemFloatXContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayElemByteX.
    def visitArrayElemByteX(self, ctx: CTE.ArrayElemByteXContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayBit.
    def visitArrayBit(self, ctx: CTE.ArrayBitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI8.
    def visitArrayI8(self, ctx: CTE.ArrayI8Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI8b.
    def visitArrayI8b(self, ctx: CTE.ArrayI8bContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI8o.
    def visitArrayI8o(self, ctx: CTE.ArrayI8oContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI8x.
    def visitArrayI8x(self, ctx: CTE.ArrayI8xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU8.
    def visitArrayU8(self, ctx: CTE.ArrayU8Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU8b.
    def visitArrayU8b(self, ctx: CTE.ArrayU8bContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU8o.
    def visitArrayU8o(self, ctx: CTE.ArrayU8oContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU8x.
    def visitArrayU8x(self, ctx: CTE.ArrayU8xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI16.
    def visitArrayI16(self, ctx: CTE.ArrayI16Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI16b.
    def visitArrayI16b(self, ctx: CTE.ArrayI16bContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI16o.
    def visitArrayI16o(self, ctx: CTE.ArrayI16oContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI16x.
    def visitArrayI16x(self, ctx: CTE.ArrayI16xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU16.
    def visitArrayU16(self, ctx: CTE.ArrayU16Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU16b.
    def visitArrayU16b(self, ctx: CTE.ArrayU16bContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU16o.
    def visitArrayU16o(self, ctx: CTE.ArrayU16oContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU16x.
    def visitArrayU16x(self, ctx: CTE.ArrayU16xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI32.
    def visitArrayI32(self, ctx: CTE.ArrayI32Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI32b.
    def visitArrayI32b(self, ctx: CTE.ArrayI32bContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI32o.
    def visitArrayI32o(self, ctx: CTE.ArrayI32oContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI32x.
    def visitArrayI32x(self, ctx: CTE.ArrayI32xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU32.
    def visitArrayU32(self, ctx: CTE.ArrayU32Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU32b.
    def visitArrayU32b(self, ctx: CTE.ArrayU32bContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU32o.
    def visitArrayU32o(self, ctx: CTE.ArrayU32oContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU32x.
    def visitArrayU32x(self, ctx: CTE.ArrayU32xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI64.
    def visitArrayI64(self, ctx: CTE.ArrayI64Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI64b.
    def visitArrayI64b(self, ctx: CTE.ArrayI64bContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI64o.
    def visitArrayI64o(self, ctx: CTE.ArrayI64oContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayI64x.
    def visitArrayI64x(self, ctx: CTE.ArrayI64xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU64.
    def visitArrayU64(self, ctx: CTE.ArrayU64Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU64b.
    def visitArrayU64b(self, ctx: CTE.ArrayU64bContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU64o.
    def visitArrayU64o(self, ctx: CTE.ArrayU64oContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayU64x.
    def visitArrayU64x(self, ctx: CTE.ArrayU64xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayF16.
    def visitArrayF16(self, ctx: CTE.ArrayF16Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayF16x.
    def visitArrayF16x(self, ctx: CTE.ArrayF16xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayF32.
    def visitArrayF32(self, ctx: CTE.ArrayF32Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayF32x.
    def visitArrayF32x(self, ctx: CTE.ArrayF32xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayF64.
    def visitArrayF64(self, ctx: CTE.ArrayF64Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#arrayF64x.
    def visitArrayF64x(self, ctx: CTE.ArrayF64xContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#customBinary.
    def visitCustomBinary(self, ctx: CTE.CustomBinaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CTE#media.
    def visitMedia(self, ctx: CTE.MediaContext):
        return self.visitChildren(ctx)


del CTE
