from textnode import TextType, TextNode
from htmlnode import HTMLNode


def main():
    t_node = TextNode("test text", TextType.LINK, "https://www.boot.dev")
    html_node = HTMLNode("div", "Hello World", None, {"class": "container"})
    print(t_node)
    print(html_node)


if __name__ == "__main__":
    main()
