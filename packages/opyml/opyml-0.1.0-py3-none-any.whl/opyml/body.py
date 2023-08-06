import json

from defusedxml import ElementTree
from typing import List, Optional
from xml.etree import ElementTree as XmlBuilder

from .outline import Outline
from .util import _dict_exclude_none


class Body:
    """The OPML Body element."""

    def __init__(self, outlines: Optional[List[Outline]] = None) -> None:
        """Create a new Body."""

        self.outlines: List[Outline] = [] if outlines is None else outlines
        """All the top-level Outline elements."""

    @staticmethod
    def from_element_tree(element: ElementTree) -> "Body":
        """Parse a Body object from an XML ElementTree."""

        return Body(Outline.parse_outlines(element))

    def insert_xml_element(self, parent: XmlBuilder.Element) -> None:
        """Insert the Body into an XML Element."""

        body = XmlBuilder.SubElement(parent, "body")
        for outline in self.outlines:
            outline.insert_xml_element(body)

    def to_json(self) -> str:
        """Output the Body as a JSON string."""

        return json.dumps(
            self,
            default=lambda o: _dict_exclude_none(o.__dict__),
            indent=2,
            sort_keys=True,
        )
