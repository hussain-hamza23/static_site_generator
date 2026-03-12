class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        return (
            " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
            if self.props
            else ""
        )

    def __repr__(self) -> str:
        return f"Tag:{self.tag},\nValue:{self.value},\nChildren:{self.children},\nProps:{self.props}"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        return (
            f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            if self.tag
            else self.value
        )

    def __repr__(self) -> str:
        return f"Tag:{self.tag},\nValue:{self.value},\nProps:{self.props}"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        return f"<{self.tag}{self.props_to_html()}>{''.join(leaf.to_html() for leaf in self.children)}</{self.tag}>"
