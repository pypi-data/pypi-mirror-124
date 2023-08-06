import json

from defusedxml import ElementTree
from typing import List, Optional
from xml.etree import ElementTree as XmlBuilder

from .util import _dict_exclude_none


class Outline:
    """The OPML Outline element."""

    def __init__(
        self,
        text: str,
        type: Optional[str] = None,
        is_comment: Optional[bool] = None,
        is_breakpoint: Optional[bool] = None,
        created: Optional[str] = None,
        category: Optional[str] = None,
        outlines: Optional[List["Outline"]] = None,
        xml_url: Optional[str] = None,
        description: Optional[str] = None,
        html_url: Optional[str] = None,
        language: Optional[str] = None,
        title: Optional[str] = None,
        version: Optional[str] = None,
        url: Optional[str] = None,
    ) -> None:
        """Create a new Outline."""

        self.text: str = text
        """Every outline element must have at least a text attribute, which is what
        is displayed when an outliner opens the OPML document.

        Version 1.0 OPML documents may omit this attribute, so for compatibility and
        strictness this attribute is “technically optional” as it will be replaced
        by an empty string if it is omitted.

        Text attributes may contain encoded HTML markup."""

        self.type: Optional[str] = type
        """A string that indicates how the other attributes of the Outline should be
        interpreted."""

        self.is_comment: Optional[bool] = is_comment
        """Indicating whether the outline is commented or not. By convention if an
        outline is commented, all subordinate outlines are considered to also be
        commented."""

        self.is_breakpoint: Optional[bool] = is_breakpoint
        """Indicating whether a breakpoint is set on this outline. This attribute is
        mainly necessary for outlines used to edit scripts."""

        self.created: Optional[str] = created
        """The date-time (RFC822) that this Outline element was created."""

        self.category: Optional[str] = category
        """A string of comma-separated slash-delimited category strings, in the
        format defined by the [RSS 2.0 category][1] element. To represent a “tag”, the
        category string should contain no slashes.
        
        [1]: https://cyber.law.harvard.edu/rss/rss.html#ltcategorygtSubelementOfLtitemgt
        """

        self.outlines: List["Outline"] = outlines if outlines is not None else []
        """Child Outline elements of the current one."""

        self.xml_url: Optional[str] = xml_url
        """The HTTP address of the feed."""

        self.description: Optional[str] = description
        """The top-level description element from the feed."""

        self.html_url: Optional[str] = html_url
        """The top-level link element from the feed."""

        self.language: Optional[str] = language
        """The top-level language element from the feed."""

        self.title: Optional[str] = title
        """The top-level title element from the feed."""

        self.version: Optional[str] = version
        """The version of the feed’s format (such as RSS 0.91, 2.0, …)."""

        self.url: Optional[str] = url
        """A link that can point to another OPML document or to something that can
        be displayed in a web browser."""

    @staticmethod
    def from_element_tree(element: ElementTree) -> "Outline":
        """Parse an Outline object from an XML ElementTree."""

        attr = element.attrib
        outline = Outline(
            text=attr.get("text", ""),
            outlines=Outline.parse_outlines(element),
        )

        if "type" in attr:
            outline.type = attr.get("type")
        if "isComment" in attr and attr.get("isComment") in ["true", "false"]:
            outline.is_comment = bool(attr.get("isComment"))
        if "isBreakpoint" in attr and attr.get("isBreakpoint") in ["true", "false"]:
            outline.is_comment = bool(attr.get("isBreakpoint"))
        if "created" in attr:
            outline.created = attr.get("created")
        if "category" in attr:
            outline.category = attr.get("category")
        if "xmlUrl" in attr:
            outline.xml_url = attr.get("xmlUrl")
        if "description" in attr:
            outline.description = attr.get("description")
        if "htmlUrl" in attr:
            outline.html_url = attr.get("htmlUrl")
        if "language" in attr:
            outline.language = attr.get("language")
        if "title" in attr:
            outline.title = attr.get("title")
        if "version" in attr:
            outline.version = attr.get("version")
        if "url" in attr:
            outline.url = attr.get("url")
        return outline

    @staticmethod
    def parse_outlines(element: ElementTree) -> List["Outline"]:
        """Parse a list of Outline elements from an XML ElementTree."""

        return list(
            map(
                lambda child: Outline.from_element_tree(child),
                filter(lambda child: child.tag == "outline", element),
            )
        )

    def insert_xml_element(self, parent: XmlBuilder.Element) -> None:
        """Insert the Outline into an XML Element."""

        outline = XmlBuilder.SubElement(parent, "outline")
        outline.attrib["text"] = self.text

        if self.text is not None:
            outline.attrib["text"] = self.text
        if self.type is not None:
            outline.attrib["type"] = self.type
        if self.is_comment is not None:
            outline.attrib["isComment"] = str(self.is_comment).lower()
        if self.is_breakpoint is not None:
            outline.attrib["isBreakpoint"] = str(self.is_breakpoint).lower()
        if self.created is not None:
            outline.attrib["created"] = self.created
        if self.category is not None:
            outline.attrib["category"] = self.category
        if self.xml_url is not None:
            outline.attrib["xmlUrl"] = self.xml_url
        if self.description is not None:
            outline.attrib["description"] = self.description
        if self.html_url is not None:
            outline.attrib["htmlUrl"] = self.html_url
        if self.language is not None:
            outline.attrib["language"] = self.language
        if self.title is not None:
            outline.attrib["title"] = self.title
        if self.version is not None:
            outline.attrib["version"] = self.version
        if self.url is not None:
            outline.attrib["url"] = self.url

        for child_outline in self.outlines:
            child_outline.insert_xml_element(outline)

    def to_json(self) -> str:
        """Output the Outline as a JSON string."""

        return json.dumps(
            self,
            default=lambda o: _dict_exclude_none(o.__dict__),
            indent=2,
            sort_keys=True,
        )
