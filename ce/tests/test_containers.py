import unittest
import ce.cte as cte
from ce.complex_types import Rid
from ce.container_types import List, Map


class ContainerListTestCase(unittest.TestCase):
    def test_simple_list(self):
        self.assertEqual(cte.load("c1 [5 4 3 2 1]"), List([5, 4, 3, 2, 1]))

    def test_simple_list_heterogeneous(self):
        self.assertEqual(
            cte.load("""c1 [5 "a" 3 2 @"foo"]"""),
            List([5, "a", 3, 2, Rid('''@"foo"''')]),
        )

    def test_simple_list_recursive(self):
        self.assertEqual(
            cte.load("""c1 [3 [2 [@"foo"]]]"""),
            List([3, List([2, List([Rid('''@"foo"''')])])]),
        )

    def test_simple_list_empty(self):
        self.assertEqual(cte.load("""c1 []"""), List([]))

class ContainerMapTestCase(unittest.TestCase):
    def test_simple_map(self):
        self.assertEqual(cte.load("""c1 {"a" = "b" }"""), Map([("a", "b")]))

    def test_simple_map_with_list(self):
        self.assertEqual(cte.load("""c1 {"a" = [1 2 3] }"""), Map([("a", List([1,2,3]))]))