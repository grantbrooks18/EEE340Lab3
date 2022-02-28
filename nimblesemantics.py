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

Group members: OCdt MacDonald and Brooks

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
        vartype = ctx.TYPE().getSymbol()
        vartype = vartype.text

        if vartype == "Int":


            if ctx.expr():
                if ctx.expr().type == PrimitiveType.Int:
                    ctx.type = PrimitiveType.Int
                else:
                    ctx.type = PrimitiveType.ERROR

            else:
                ctx.type = PrimitiveType.Int

        elif vartype == "Bool":
            # todo Test if the data is an bool
            ctx.type = PrimitiveType.Bool

        elif vartype == "String":
            # todo Test if the data is an string

            ctx.type = PrimitiveType.String

        else:
            ctx.type = PrimitiveType.ERROR

        newkey = str(ctx.ID())

        self.variables[newkey] = ctx.type

        print(self.variables)

    # --------------------------------------------------------
    # Statements
    # --------------------------------------------------------

    def exitAssignment(self, ctx: NimbleParser.AssignmentContext):
        pass

    def exitWhile(self, ctx: NimbleParser.WhileContext):
        if ctx.expr().type != PrimitiveType.Bool:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.CONDITION_NOT_BOOL,
                               f"Expression {ctx.expr().text} not boolean")
            return

    def exitIf(self, ctx: NimbleParser.IfContext):

        if ctx.expr().type != PrimitiveType.Bool:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.CONDITION_NOT_BOOL,
                               f"Expression {ctx.expr().text} not boolean")
            return

    def exitPrint(self, ctx: NimbleParser.PrintContext):

        if ctx.expr().type == PrimitiveType.ERROR:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.UNPRINTABLE_EXPRESSION,
                               f"Can't print {ctx.op.text} ")

    # --------------------------------------------------------
    # Expressions
    # --------------------------------------------------------

    def exitIntLiteral(self, ctx: NimbleParser.IntLiteralContext):
        ctx.type = PrimitiveType.Int

    def exitNeg(self, ctx: NimbleParser.NegContext):

        if ctx.op.text == '-' and ctx.expr().type == PrimitiveType.Int:
            ctx.type = PrimitiveType.Int
        elif ctx.op.text == '-':  # if !is used on non ints
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_NEGATION,
                               f"Can't apply {ctx.op.text} to {ctx.expr().type.name}")

        if ctx.op.text == '!' and ctx.expr().type == PrimitiveType.Bool:
            ctx.type = PrimitiveType.Bool
        elif ctx.op.text == '!':  # if ! is used on non bools
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_NEGATION,
                               f"Can't apply {ctx.op.text} to {ctx.expr().type.name}")

    def exitParens(self, ctx: NimbleParser.ParensContext):
        ctx.type = ctx.expr().type

    def exitMulDiv(self, ctx: NimbleParser.MulDivContext):
        if ctx.expr(0).type == PrimitiveType.Int and ctx.expr(1).type == PrimitiveType.Int:
            ctx.type = PrimitiveType.Int
        else:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_BINARY_OP,
                               f"Can't apply {ctx.op.text} to {ctx.expr(0).type.name} and {ctx.expr(1).type.name}")

    def exitAddSub(self, ctx: NimbleParser.AddSubContext):

        if ctx.expr(0).type == PrimitiveType.Int and ctx.expr(1).type == PrimitiveType.Int:
            ctx.type = PrimitiveType.Int
            return
        elif ctx.expr(0).type == PrimitiveType.String and ctx.expr(
                1).type == PrimitiveType.String and ctx.op.text == '+':
            ctx.type = PrimitiveType.String
            return

        ctx.type = PrimitiveType.ERROR
        self.error_log.add(ctx, Category.INVALID_BINARY_OP,
                           f"Can't apply {ctx.op.text} to {ctx.expr(0).type.name} and {ctx.expr(1).type.name}")

    def exitCompare(self, ctx: NimbleParser.CompareContext):

        if ctx.expr(0).type == PrimitiveType.Int and ctx.expr(1).type == PrimitiveType.Int:
            ctx.type = PrimitiveType.Bool
        else:
            ctx.type = PrimitiveType.ERROR
            self.error_log.add(ctx, Category.INVALID_BINARY_OP,
                               f"Can't apply {ctx.op.text} to {ctx.expr(0).type.name} and {ctx.expr(1).type.name}")

    def exitVariable(self, ctx: NimbleParser.VariableContext):
        pass

    def exitStringLiteral(self, ctx: NimbleParser.StringLiteralContext):
        ctx.type = PrimitiveType.String

    def exitBoolLiteral(self, ctx: NimbleParser.BoolLiteralContext):
        ctx.type = PrimitiveType.Bool
