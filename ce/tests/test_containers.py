import os
import unittest
import ce.cte as cte
from decimal import Decimal
from ce.primitive_types import BinaryFloat
from ce.complex_types import Rid
from ce.container_types import Map


class ContainerListTestCase(unittest.TestCase):
    def test_simple_list(self):
        self.assertEqual(cte.load("c1 [5 4 3 2 1]"), [5, 4, 3, 2, 1])

    def test_simple_list_heterogeneous(self):
        self.assertEqual(
            cte.load("""c1 [5 "a" 3 2 @"foo"]"""),
            [5, "a", 3, 2, Rid('''@"foo"''')],
        )

    def test_simple_list_recursive(self):
        self.assertEqual(
            cte.load("""c1 [3 [2 [@"foo"]]]"""),
            [3, [2, [Rid('''@"foo"''')]]],
        )

    def test_simple_list_empty(self):
        self.assertEqual(cte.load("""c1 []"""), [])

class ContainerMapTestCase(unittest.TestCase):
    def test_simple_map(self):
        self.assertEqual(cte.load("""c1 {"a" = "b" }"""), Map([("a", "b")]))

    def test_simple_map_with_list(self):
        self.assertEqual(cte.load("""c1 {"a" = [1 2 3] }"""), Map([("a", [1,2,3])]))

    def test_nested_map(self):
        self.assertEqual(cte.load("""c1 {"a" = {"b" = "c"} }"""), Map([("a", Map([("b", "c")]))]))

    def test_numeric_cte(self):

        self.maxDiff = None

        filename = os.path.join(
            os.path.dirname(__file__), "examples/numeric_map.cte"
        )

        expected = Map([
            ('boolean', True), 
            ('binary int', -139),
            ('octal int', 420),
            ('decimal int', -10000000),
            ('hex int', 4294836225), 
            ('very long int', 100000000000000000000000000000000000009),
            ('decimal float', Decimal('-14.125')),
            ('hex float', BinaryFloat("0x5.1ec4p+20")), 
            ('very long flt', Decimal('4.957234990634579394723460546348E+100000')),
            ('infinity', Decimal('Infinity')),
            ('neg infinity', Decimal('-Infinity'))
        ])
        with open(filename, "r") as f:
            test = f.read()
            self.assertEqual(cte.load(test), expected)