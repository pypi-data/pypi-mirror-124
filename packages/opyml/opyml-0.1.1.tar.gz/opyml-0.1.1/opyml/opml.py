import json

from defusedxml import ElementTree
from typing import Optional
from xml.etree import ElementTree as XmlBuilder

from .body import Body
from .head import Head
from .util import _dict_exclude_none


class OPML:
    """The root OPML element."""

    def __init__(
        self,
        version: Optional[str] = None,
        head: Optional[Head] = None,
        body: Optional[Body] = None,
    ) -> None:
        """Create a new OPML document."""

        self.version: str = version if version is not None else "2.0"
        """The OPML spec version of this document.

        Must be `1.0`, `1.1` or `2.0`."""
        if self.version not in ["1.0", "1.1", "2.0"]:
            raise ValueError(f"unsupported version: {version}")

        self.head: Optional[Head] = head
        """The Head child object. Contains the metadata of the OPML document."""

        self.body: Body = Body() if body is None else body
        """The Body child object. Contains all the Outline elements."""

    @staticmethod
    def from_xml(xml: str) -> "OPML":
        """Parse an OPML document from an XML string."""

        root = ElementTree.fromstring(xml)

        if root.tag != "opml":
            raise ValueError("root element is not <opml>")

        # OPML elements must have a version attribute.
        if "version" not in root.attrib:
            raise ValueError("missing <opml> version attribute")

        # And the version attribute can only be 1.0, 1.1 or 2.0.
        version = root.attrib.get("version")
        if version not in ["1.0", "1.1", "2.0"]:
            raise ValueError(f"unsupported version: {version}")

        # OPML elements must have a <body> child element.
        if True not in map(lambda e: e.tag == "body", root):
            raise ValueError("root <opml> element is missing a child <body>")

        opml = OPML(version)

        for child in root:
            if child.tag == "head":
                opml.head = Head.from_element_tree(child)
            elif child.tag == "body":
                opml.body = Body.from_element_tree(child)

        # OPML documents must contain at least 1 <outline> element.
        if len(opml.body.outlines) == 0:
            raise ValueError("<body> contains no <outline> elements")

        return opml

    def to_xml(self) -> str:
        """Output the OPML document as an XML string."""

        opml = XmlBuilder.Element("opml")
        opml.attrib["version"] = self.version

        if self.head is not None:
            self.head.insert_xml_element(opml)

        self.body.insert_xml_element(opml)
        return XmlBuilder.tostring(opml, encoding="unicode")

    def to_json(self) -> str:
        """Output the OPML document as a JSON string."""

        return json.dumps(
            self,
            default=lambda o: _dict_exclude_none(o.__dict__),
            indent=2,
            sort_keys=True,
        )
