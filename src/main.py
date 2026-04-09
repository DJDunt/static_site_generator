from textnode import TextNode, TextType,text_node_to_html_node

def main():
    # 1. Test Plain Text
    node_text = TextNode("Just some text", TextType.TEXT)
    html_node_text = text_node_to_html_node(node_text)
    print(f"Text: {html_node_text.to_html()}")

    # 2. Test Bold
    node_bold = TextNode("Strong words", TextType.BOLD)
    html_node_bold = text_node_to_html_node(node_bold)
    print(f"Bold: {html_node_bold.to_html()}")

    # 3. Test Bold
    node_italic = TextNode("Italic words", TextType.ITALIC)
    html_node_italic = text_node_to_html_node(node_italic)
    print(f"Italic: {html_node_italic.to_html()}")

    # 4. Test Link
    node_link = TextNode("Click me!", TextType.LINK, "https://www.boot.dev")
    html_node_link = text_node_to_html_node(node_link)
    print(f"Link: {html_node_link.to_html()}")

    # 5. Test Image
    node_img = TextNode("A brave wizard bear", TextType.IMAGE, "https://boot.dev/img.png")
    html_node_img = text_node_to_html_node(node_img)
    print(f"Image: {html_node_img.to_html()}")

if __name__ == "__main__":
    main()