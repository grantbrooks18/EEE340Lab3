"""
Test cases for Nimble semantic analysis. See also the `testhelpers`
module.

Test harnesses have been provided for testing correct semantic
analysis of valid and invalid expressions.

**You will need to provide your own testing mechanisms for statements and
higher-level constructs as appropriate.**


Group members: Grant Brooks, Connor MacDonald

Version: 28/02/2022
Instructor's version: 2022-02-04
"""

import unittest

from errorlog import Category
from symboltable import PrimitiveType
from testhelpers import do_semantic_analysis, pretty_types, do_semantic_analysis_initial_condition

VALID_EXPRESSIONS = [
    # Each entry is a pair: (expression source, expected type)
    # Due to the way the inferred_types are stored, using ctx.getText() as the key,
    # expressions must contain NO WHITE SPACE for the tests to work. E.g.,
    # '59+a' is fine, '59 + a' won't work.
    ('37', PrimitiveType.Int),
    ('-37', PrimitiveType.Int),

    ('true', PrimitiveType.Bool),
    ('false', PrimitiveType.Bool),

    ('!false', PrimitiveType.Bool),
    ('true', PrimitiveType.Bool),
    ('!true', PrimitiveType.Bool),

    ('(37)', PrimitiveType.Int),
    ('(-37)', PrimitiveType.Int),
    ('(true)', PrimitiveType.Bool),
    ('(!false)', PrimitiveType.Bool),

    ('"abcdef"', PrimitiveType.String),
    ('"Hel  l O  !"', PrimitiveType.String),
    ('"Hel  \\a\\nl"', PrimitiveType.String),

    ('1<2', PrimitiveType.Bool),
    ('(1==2)', PrimitiveType.Bool),
    ('(1==-2)', PrimitiveType.Bool),

    ('1+2', PrimitiveType.Int),
    ('(1--2)', PrimitiveType.Int),
    ('"HELLO"+"WORLD"', PrimitiveType.String),

    ('1*3', PrimitiveType.Int),
    ('(1/2*4)', PrimitiveType.Int),
    ('((1*2)/4*-2)', PrimitiveType.Int),

]

INVALID_EXPRESSIONS = [
    # Each entry is a pair: (expression source, expected error category)
    # As for VALID_EXPRESSIONS, there should be NO WHITE SPACE in the expressions.
    ('!37', Category.INVALID_NEGATION),
    ('!!37', Category.INVALID_NEGATION),

    ('-true', Category.INVALID_NEGATION),
    ('-false', Category.INVALID_NEGATION),

    ('true<3', Category.INVALID_BINARY_OP),
    ('true<!false', Category.INVALID_BINARY_OP),
    ('!true==false', Category.INVALID_BINARY_OP),

    ('"HELLO"-"WORLD"', Category.INVALID_BINARY_OP),
    ('true+false', Category.INVALID_BINARY_OP),
    ('true-4', Category.INVALID_BINARY_OP),
    ('"abc"+false', Category.INVALID_BINARY_OP),

    ('"HELLO"-"WORLD"', Category.INVALID_BINARY_OP),
    ('true+false', Category.INVALID_BINARY_OP),
    ('true-4', Category.INVALID_BINARY_OP),
    ('"abc"+false', Category.INVALID_BINARY_OP),

    ('"HELLO"/"WORLD"', Category.INVALID_BINARY_OP),
    ('true*false', Category.INVALID_BINARY_OP),
    ('true*4', Category.INVALID_BINARY_OP),
    ('"abc"/false', Category.INVALID_BINARY_OP),

]

VARDEC_TESTS = [

    ("var Apple : Int", PrimitiveType.Int, "Apple"),
    ("var Apple : Int = 1 ", PrimitiveType.Int, "Apple"),
    ("var Apple : Int = true ", PrimitiveType.ERROR, "Apple"),
    ("var Apple : Int = \"Hello\" ", PrimitiveType.ERROR, "Apple"),


    ("var Pear : Bool = true ", PrimitiveType.Bool, "Pear"),
    ("var Pear : Bool = false ", PrimitiveType.Bool, "Pear"),
    ("var Pear : Bool = \"Hello\" ", PrimitiveType.ERROR, "Pear"),
    ("var Pear : Bool = 654 ", PrimitiveType.ERROR, "Pear"),
    ("var Pear : Bool", PrimitiveType.Bool, "Pear"),


    ("var nectarine : String = 654 ", PrimitiveType.ERROR, "nectarine"),
    ("var nectarine : String = \"Hello\" ", PrimitiveType.String, "nectarine"),
    ("var nectarine : String = true ", PrimitiveType.ERROR, "nectarine"),
    ("var nectarine : String", PrimitiveType.String, "nectarine"),
]

VARASSIGN_TESTS_valid = [
    ("Apple = 1", PrimitiveType.Int, "Apple",{"Apple" : PrimitiveType.Int} ),
    ("Pear = true", PrimitiveType.Bool,"Pear", {"Pear" : PrimitiveType.Bool}),
    ("nectarine = \"The Best Fruit\"", PrimitiveType.String,"nectarine", {"nectarine": PrimitiveType.String }),
]

VARASSIGN_TESTS_invalid = [
    ("Apple = true", PrimitiveType.ERROR,  "Apple",{"Apple" : PrimitiveType.Int}),
    ("Apple = \"Hello\"", PrimitiveType.ERROR,  "Apple",{"Apple" : PrimitiveType.Int}),
    ("Apple = 1", PrimitiveType.ERROR,  "Apple",{"Apple" : PrimitiveType.ERROR}),

    ("Pear = 5", PrimitiveType.ERROR, "Pear",{"Pear" : PrimitiveType.Bool}),
    ("Pear = \"Hello\"", PrimitiveType.ERROR, "Pear",{"Pear" : PrimitiveType.Bool}),
    ("Pear = true", PrimitiveType.ERROR, "Pear",{"Pear" : PrimitiveType.ERROR}),

    ("nectarine = 5", PrimitiveType.ERROR, "nectarine", {"nectarine": PrimitiveType.String }),
    ("nectarine = true", PrimitiveType.ERROR, "nectarine", {"nectarine": PrimitiveType.String }),
    ("nectarine = \"Hello\"", PrimitiveType.ERROR, "nectarine", {"nectarine": PrimitiveType.ERROR }),


]


def print_debug_info(source, inferred_types, log):
    """
    Can be called from test cases when things aren't going as expected
    and you need a look at the inferred types and error log. See commented-out
    examples in test_valid_expressions and test_invalid_expressions below
    """
    print('\n------------------------------')
    print(f'{source}\n')
    print(pretty_types(inferred_types))
    if log.total_entries():
        print(f'\n{log}')


class TypeTests(unittest.TestCase):

    def test_valid_expressions(self):
        """
        For each pair (expression source, expected type) in VALID_EXPRESSIONS, verifies
        that the expression's inferred type is as expected, and that there are no errors
        in the error log.
        """
        for expression, expected_type in VALID_EXPRESSIONS:
            log, variables, inferred_types = do_semantic_analysis(expression, 'expr')
            # if expression == '-37':
            #     print_debug_info(expression, inferred_types, log)
            with self.subTest(expression=expression, expected_type=expected_type):
                self.assertEqual(expected_type, inferred_types[1][expression])
                self.assertEqual(0, log.total_entries())

    def test_invalid_expressions(self):
        """
        For each pair (expression source, expected error category) in INVALID_EXPRESSIONS,
        verifies that the expression is assigned the ERROR type and that there is a logged
        error of the expected category relating to the expression.
        """
        for expression, expected_category in INVALID_EXPRESSIONS:
            log, variables, inferred_types = do_semantic_analysis(expression, 'expr')
            # if expression == '!!37':
            #     print_debug_info(expression, inferred_types, log)
            with self.subTest(expression=expression,
                              expected_category=expected_category):
                self.assertEqual(PrimitiveType.ERROR, inferred_types[1][expression])
                self.assertTrue(log.includes_exactly(expected_category, 1, expression))

    def test_variable_Declaration(self):
        """
        This was stolen from the above examples to rapidly loop through variables and see if they match their types.

        This testcase uses a third field that is just the ID to allow for lookup of the
        variable in the variable dictionary
        """

        for expression, expected_type, ID in VARDEC_TESTS:
            log, variables, inferred_types = do_semantic_analysis(expression, 'varDec')
            # if expression == '-37':
            #     print_debug_info(expression, inferred_types, log)
            with self.subTest(expression=expression, expected_type=expected_type):
                self.assertEqual(expected_type, variables[ID])



    def test_variable_assignment(self):
        """
        This was stolen from the above examples to rapidly loop through variables and see if they match their types.

        This testcase uses a third field that is just the ID to allow for lookup of the
        variable in the variable dictionary
        """

        for expression, expected_type, ID, setup in VARASSIGN_TESTS_valid:
            log, variables, inferred_types = do_semantic_analysis_initial_condition(expression, 'statement',setup)
            with self.subTest(expression=expression, expected_type=expected_type):
                self.assertEqual(expected_type, variables[ID])
                self.assertEqual(0, log.total_entries())

        for expression, expected_type, ID, setup in VARASSIGN_TESTS_invalid:
            log, variables, inferred_types = do_semantic_analysis_initial_condition(expression, 'statement', setup)
            with self.subTest(expression=expression, expected_type=expected_type):
                self.assertEqual(expected_type, variables[ID])
                self.assertEqual(1, log.total_entries())

    def test_print_primitive(self):
        log, variables, inferred_types = do_semantic_analysis("print 123", 'main')
        self.assertEqual(0, log.total_entries())

        log, variables, inferred_types = do_semantic_analysis('print "hello"', 'main')
        self.assertEqual(0, log.total_entries())

        log, variables, inferred_types = do_semantic_analysis("print true", 'main')
        self.assertEqual(0, log.total_entries())

    def test_if_while_primitive(self):
        log, variables, inferred_types = do_semantic_analysis("if true { }", 'main')
        self.assertEqual(0, log.total_entries())

        log, variables, inferred_types = do_semantic_analysis('if true { } else { }', 'main')
        self.assertEqual(0, log.total_entries())

        log, variables, inferred_types = do_semantic_analysis("while true { }", 'main')
        self.assertEqual(0, log.total_entries())
