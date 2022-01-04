import unittest
import ce.cte as cte
from ce.complex_types import Rid


class ContainerListTestCase(unittest.TestCase):
    def test_simple_container(self):
        self.assertEqual(cte.load("c1 [5 4 3 2 1]"), [5, 4, 3, 2, 1])

    def test_simple_container_heterogeneous(self):
        self.assertEqual(
            cte.load("""c1 [5 "a" 3 2 @"foo"]"""), [5, "a", 3, 2, Rid('''@"foo"''')]
        )

    def test_simple_container_recursive(self):
        self.assertEqual(
            cte.load("""c1 [5 ["a" [3 [2 [@"foo"]]]]]"""),
            [5, ["a", [3, [2, [Rid('''@"foo"''')]]]]],
        )
