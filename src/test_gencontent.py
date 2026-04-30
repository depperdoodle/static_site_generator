import unittest
from gencontent import extract_title

class TestInlineMarkdown(unittest.TestCase):

    def test_eq(self):
        actual = extract_title("# Hello")
        self.assertEqual(actual, "Hello")

if __name__ == "__main__":
    unittest.main()