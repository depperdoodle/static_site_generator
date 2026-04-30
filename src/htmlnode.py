import html


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        s = ''.join(f' {k}="{v}"' for k, v in self.props.items())
        return(s)
 
    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return (f"LeafNode({self.tag}, {self.value}, {self.props})")
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
            if not self.tag:
                raise ValueError(f"Like, zoinks, Scoob!")
            if not self.children:
                raise ValueError(f"Uh oh, Raggie!")
            else:
                result = ""
                for item in self.children:
                    result += item.to_html()
                return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"