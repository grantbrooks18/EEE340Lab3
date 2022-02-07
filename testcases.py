"""
Test cases for Nimble semantic analysis. See also the `testhelpers`
module.

Test harnesses have been provided for testing correct semantic
analysis of valid and invalid expressions.

**You will need to provide your own testing mechanisms for statements and
higher-level constructs as appropriate.**

TODO: Complete test cases for Nimble semantic analysis, less function definitions and calls

Group members: TODO: Your names here

Version: TODO: Submission date here
Instructor's version: 2022-02-04
"""

import unittest

from errorlog import Category
from symboltable import PrimitiveType
from testhelpers import do_semantic_analysis, pretty_types

VALID_EXPRESSIONS = [
    # Each entry is a pair: (expression source, expected type)
    # Due to the way the inferred_types are stored, using ctx.getText() as the key,
    # expressions must contain NO WHITE SPACE for the tests to work. E.g.,
    # '59+a' is fine, '59 + a' won't work.
    ('37', PrimitiveType.Int),
    ('-37', PrimitiveType.Int)
]

INVALID_EXPRESSIONS = [
    # Each entry is a pair: (expression source, expected error category)
    # As for VALID_EXPRESSIONS, there should be NO WHITE SPACE in the expressions.
    ('!37', Category.INVALID_NEGATION),
    ('!!37', Category.INVALID_NEGATION),
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