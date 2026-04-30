import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "let's get into all that hub bub", [], {"href": "https://www.google.com"})
        result = node.props_to_html()
        self.assertEqual(result, " href=\"https://www.google.com\"")

    def test_not_eq(self):
        node = HTMLNode("h1", "let's get into all that hub bub", [], {"href": "https://www.hub-bub.com"})
        result = node.props_to_html()
        self.assertEqual(result, " href=\"https://www.hub-bub.com\"")

    def test_no_props(self):
        node = HTMLNode("h1", "let's get into all that hub bub", [], None)
        self.assertIsNone(node.props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p2(self):
        node = LeafNode("p", "Bub hub bub!")
        self.assertEqual(node.to_html(), "<p>Bub hub bub!</p>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just some raw text.")
        self.assertEqual(node.to_html(), "Just some raw text.")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    

if __name__ == "__main__":
    unittest.main()