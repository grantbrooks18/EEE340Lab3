"""
The nimblesemantics module contains the logic required to perform a semantic
analysis of any syntactically-correct Nimble program, not including function
definitions and function calls.

TODO: Implement to make this true.

The analysis has two major tasks:

- to infer the types of all *expressions* in a Nimble program (including ERROR types)
and to add appropriate type annotations to the program's ANTLR-generated syntax tree
by adding a `type` attribute to each expression node; and

- to identify and flag all violations of the Nimble semantic specification
using the errorlog module.

In order to do this, it is necessary to record all declared variable types in the
`variables` dictionary.

Group members: TODO: Your names here

Version: TODO: Submission date here

"""

from errorlog import ErrorLog, Category
from nimble import NimbleListener, NimbleParser
from symboltable import PrimitiveType


class InferTypesAndCheckConstraints(NimbleListener):
    """
    The type of each expression parse tree node is calculated and attached to the node as a
    `type` attribute, e.g,. ctx.type = ...

    The types of declared variables are stored in `self.variables`, which is a dictionary
    mapping from variable names to symboltable.PrimitiveType instances.

    Any semantic errors detected, e.g., undefined variable names,
    type mismatches, etc, are logged in the `error_log`
    """

    def __init__(self, error_log: ErrorLog, variables: dict):
        self.error_log = error_log
        self.variables = variables

    # --------------------------------------------------------
    # Program structure
    # --------------------------------------------------------

    def exitScript(self, ctx: NimbleParser.ScriptContext):
        pass

    def exitMain(self, ctx: NimbleParser.MainContext):
        pass

    def exitBody(self, ctx: NimbleParser.BodyContext):
        pass

    def exitVarBlock(self, ctx: NimbleParser.VarBlockContext):
        pass

    def exitBlock(self, ctx: NimbleParser.BlockContext):
        pass

    # --------------------------------------------------------
    # Variable declarations
    # --------------------------------------------------------

    def exitVarDec(self, ctx: NimbleParser.VarDecContext):
        pass

    # --------------------------------------------------------
    # Statements
    # --------------------------------------------------------

    def exitAssignment(self, ctx: NimbleParser.AssignmentContext):
        pass

    def exitWhile(self, ctx: NimbleParser.WhileContext):
        pass

    def exitIf(self, ctx: NimbleParser.IfContext):
        pass

    def exitPrint(self, ctx: NimbleParser.PrintContext):
        pass

    # --------------------------------------------------------
    # Expressions
    # --------------------------------------------------------

    def exitIntLiteral(self, ctx: NimbleParser.IntLiteralContext):
        ctx.type = PrimitiveType.Int

    def exitNeg(self, ctx: NimbleParser.NegContext):
        """ TODO: Extend to handle boolean negation. """
        if ctx.op.text == '-' and ctx.expr().type == PrimitiveType.Int:
            ctx.type = PrimitiveType.Int
        else:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_NEGATION,
                               f"Can't apply {ctx.op.text} to {ctx.expr().type.name}")

    def exitParens(self, ctx: NimbleParser.ParensContext):
        pass

    def exitMulDiv(self, ctx: NimbleParser.MulDivContext):
        pass

    def exitAddSub(self, ctx: NimbleParser.AddSubContext):
        pass

    def exitCompare(self, ctx: NimbleParser.CompareContext):
        pass

    def exitVariable(self, ctx: NimbleParser.VariableContext):
        pass

    def exitStringLiteral(self, ctx: NimbleParser.StringLiteralContext):
        pass

    def exitBoolLiteral(self, ctx: NimbleParser.BoolLiteralContext):
        pass
