import unittest
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link,
    text_to_textnodes
    )
from textnode import TextNode, TextType

class test_InlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):

        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_italic(self):

        nodes = [TextNode("This is *italic* text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_code(self):

        nodes = [TextNode("This is `code` text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_unclosed(self):

        nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            str(context.exception), "Thats invlid markdown, delimiter ** is not closed"
        )
    
    def test_split_nodes_delimiter_empty(self):

        nodes = [TextNode("This is **** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_non_text_node(self):

        nodes = [TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev"),
            ],
        )

    def test_split_nodes_delimiter_multiple(self):

        nodes = [TextNode("This is **bold** and *italic* text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )   

    def test_split_nodes_delimiter_no_delimiters(self):
        nodes = [TextNode("This is plain text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is plain text", TextType.TEXT),
            ],
        )

    def test_extract_markdown_images(self):
        text = "This is an image ![alt text](https://www.boot.dev/image.png) in markdown"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt text", "https://www.boot.dev/image.png")])

    def test_extract_markdown_links(self):
        text = "This is a link [Boot.dev](https://www.boot.dev) in markdown"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("Boot.dev", "https://www.boot.dev")])

    def test_extract_markdown_links_no_links(self):
        text = "This is plain text with no links"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])

    def test_extract_markdown_images_no_images(self):
        text = "This is plain text with no images"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

    def test_extract_markdown_links_with_images(self):
        text = "This is a link [Boot.dev](https://www.boot.dev) and an image ![alt text](https://www.boot.dev/image.png) in markdown"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("Boot.dev", "https://www.boot.dev")])

    def test_extract_markdown_images_with_links(self):
        text = "This is a link [Boot.dev](https://www.boot.dev) and an image ![alt text](https://www.boot.dev/image.png) in markdown"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt text", "https://www.boot.dev/image.png")])  
    
    def test_split_nodes_image(self):
        nodes = [TextNode("This is an image ![alt text](https://www.boot.dev/image.png) in markdown", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://www.boot.dev/image.png"),
                TextNode(" in markdown", TextType.TEXT),
            ],
        )
    
    def test_split_nodes_link(self):
        nodes = [TextNode("This is a link [Boot.dev](https://www.boot.dev) in markdown", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a link ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" in markdown", TextType.TEXT),
            ],
        )

    def test_split_nodes_no_images(self):
        nodes = [TextNode("This is plain text with no images", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is plain text with no images", TextType.TEXT),
            ],
        )

    def test_split_nodes_no_links(self):
        nodes = [TextNode("This is plain text with no links", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is plain text with no links", TextType.TEXT),
            ],
        )

    def test_split_nodes_starts_with_image(self):
        nodes = [TextNode("![alt text](https://www.boot.dev/image.png) is an image in markdown", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("alt text", TextType.IMAGE, "https://www.boot.dev/image.png"),
                TextNode(" is an image in markdown", TextType.TEXT),
            ],
        )

    def test_split_nodes_ends_with_image(self):
        nodes = [TextNode("This is an image in markdown ![alt text](https://www.boot.dev/image.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an image in markdown ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://www.boot.dev/image.png"),
            ],
        )

    def test_split_nodes_starts_with_link(self):
        nodes = [TextNode("[Boot.dev](https://www.boot.dev) is a link in markdown", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is a link in markdown", TextType.TEXT),
            ],
        )

    def test_split_nodes_ends_with_link(self):
        nodes = [TextNode("This is a link in markdown [Boot.dev](https://www.boot.dev)", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a link in markdown ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            ],
        )

    def test_split_nodes_multiple_images(self):
        nodes = [TextNode("This is an image ![alt text](https://www.boot.dev/image.png) and another image ![alt text 2](https://www.boot.dev/image2.png) in markdown", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://www.boot.dev/image.png"),
                TextNode(" and another image ", TextType.TEXT),
                TextNode("alt text 2", TextType.IMAGE, "https://www.boot.dev/image2.png"),
                TextNode(" in markdown", TextType.TEXT),
            ],
        )

    def test_split_nodes_multiple_links(self):
        nodes = [TextNode("This is a link [Boot.dev](https://www.boot.dev) and another link [Google](https://www.google.com) in markdown", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a link ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another link ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://www.google.com"),
                TextNode(" in markdown", TextType.TEXT),
            ],
        )

    def test_split_nodes_TextType_not_TEXT(self):
        nodes = [TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev/image.png")]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev/image.png"),
            ],
        )
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev/image.png"),
            ],
        )

    def test_text_to_textnode_plain_text(self):
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is plain text", TextType.TEXT),
            ],
        )
 
    def test_text_to_textnode_one_bold(self):
        text = "This is **bold** text in markdown"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text in markdown", TextType.TEXT),
            ],
        )

    def test_text_to_textnode_one_italic(self):
        text = "This is _italic_ text in markdown"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text in markdown", TextType.TEXT),
            ],
        )

    def test_text_to_textnode_one_code_block(self):
        text = "This is a code block `code` in markdown"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is a code block ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" in markdown", TextType.TEXT),
            ],
        )

    def test_text_to_textnode_combined(self):
        text = "This is **bold** and _italic_ text with a link [Boot.dev](https://www.boot.dev) and an image ![alt text](https://www.boot.dev/image.png) in markdown"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text with a link ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://www.boot.dev/image.png"),
                TextNode(" in markdown", TextType.TEXT),
            ],
        )

if __name__ == "__main__":
    unittest.main()        