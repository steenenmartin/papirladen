from typing import Union
from xml.dom.minidom import Document, Element


class XmlHelper:
    def __init__(self, xml: Union[Document, Element]):
        self.xml = xml

    def get_element_by_tag_name(self, tag_name, filter_func=lambda x: True) -> str:
        [element] = self.get_elements_by_tag_name(tag_name, filter_func)

        if element.firstChild is None:
            return ""

        return element.firstChild.data

    def get_elements_by_tag_name(self, tag_name, filter_func=lambda x: True) -> list[Element]:
        return [element for element in self.xml.getElementsByTagName(tag_name) if filter_func(element)]

    @staticmethod
    def prettify(element, indent='  '):
        queue = [(0, element)]  # (level, element)
        while queue:
            level, element = queue.pop(0)
            children = [(level + 1, child) for child in list(element)]
            if children:
                # for child open
                element.text = '\n' + indent * (level + 1)

            if queue:
                # for sibling open
                element.tail = '\n' + indent * queue[0][0]
            else:
                # for parent close
                element.tail = '\n' + indent * (level - 1)

            # prepend so children come before siblings
            queue[0:0] = children
