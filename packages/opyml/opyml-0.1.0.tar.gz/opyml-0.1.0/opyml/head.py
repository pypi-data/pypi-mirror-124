import json

from defusedxml import ElementTree
from typing import Optional
from xml.etree import ElementTree as XmlBuilder

from .util import _dict_exclude_none


class Head:
    """The OPML Head element."""

    def __init__(
        self,
        title: Optional[str] = None,
        date_created: Optional[str] = None,
        date_modified: Optional[str] = None,
        owner_name: Optional[str] = None,
        owner_email: Optional[str] = None,
        owner_id: Optional[str] = None,
        docs: Optional[str] = None,
        expansion_state: Optional[str] = None,
        vert_scroll_state: Optional[int] = None,
        window_top: Optional[int] = None,
        window_left: Optional[int] = None,
        window_bottom: Optional[int] = None,
        window_right: Optional[int] = None,
    ) -> None:
        """Create a new Head."""

        self.title: Optional[str] = title
        """The title of the document."""

        self.date_created: Optional[str] = date_created
        """A date-time (RFC822) indicating when the document was created."""

        self.date_modified: Optional[str] = date_modified
        """A date-time (RFC822) indicating when the document was last modified."""

        self.owner_name: Optional[str] = owner_name
        """The name of the document owner."""

        self.owner_email: Optional[str] = owner_email
        """The email address of the document owner."""

        self.owner_id: Optional[str] = owner_id
        """A link to the website of the document owner."""

        self.docs: Optional[str] = docs
        """A link to the documentation of the OPML format used for this document."""

        self.expansion_state: Optional[str] = expansion_state
        """A comma-separated list of line numbers that are expanded. The line
        numbers in the list tell you which headlines to expand. The order is
        important. For each element in the list, X, starting at the first summit,
        navigate flatdown X times and expand. Repeat for each element in the
        list."""

        self.vert_scroll_state: Optional[int] = vert_scroll_state
        """A number indicating which line of the outline is displayed on the top
        line of the window. This number is calculated with the expansion state
        already applied."""

        self.window_top: Optional[int] = window_top
        """The pixel location of the top edge of the window."""

        self.window_left: Optional[int] = window_left
        """The pixel location of the left edge of the window."""

        self.window_bottom: Optional[int] = window_bottom
        """The pixel location of the bottom edge of the window."""

        self.window_right: Optional[int] = window_right
        """The pixel location of the right edge of the window."""

    @staticmethod
    def from_element_tree(element: ElementTree) -> "Head":
        """Parse a Head object from an XML ElementTree."""

        head = Head()
        for child in element:
            if child.tag == "title":
                head.title = child.text
            elif child.tag == "dateCreated":
                head.date_created = child.text
            elif child.tag == "dateModified":
                head.date_modified = child.text
            elif child.tag == "ownerName":
                head.owner_name = child.text
            elif child.tag == "ownerEmail":
                head.owner_email = child.text
            elif child.tag == "ownerId":
                head.owner_id = child.text
            elif child.tag == "docs":
                head.docs = child.text
            elif child.tag == "expansionState":
                head.expansion_state = child.text
            elif child.tag == "vertScrollState":
                head.vert_scroll_state = int(child.text)
            elif child.tag == "windowTop":
                head.window_top = int(child.text)
            elif child.tag == "windowLeft":
                head.window_left = int(child.text)
            elif child.tag == "windowBottom":
                head.window_bottom = int(child.text)
            elif child.tag == "windowRight":
                head.window_right = int(child.text)
        return head

    def insert_xml_element(self, parent: XmlBuilder.Element) -> None:
        """Insert the Head into an XML Element."""

        head = XmlBuilder.SubElement(parent, "head")
        if self.title is not None:
            element = XmlBuilder.SubElement(head, "title")
            element.text = self.title
        if self.date_created is not None:
            element = XmlBuilder.SubElement(head, "dateCreated")
            element.text = self.date_created
        if self.date_modified is not None:
            element = XmlBuilder.SubElement(head, "dateModified")
            element.text = self.date_modified
        if self.owner_name is not None:
            element = XmlBuilder.SubElement(head, "ownerName")
            element.text = self.owner_name
        if self.owner_email is not None:
            element = XmlBuilder.SubElement(head, "ownerEmail")
            element.text = self.owner_email
        if self.owner_id is not None:
            element = XmlBuilder.SubElement(head, "ownerId")
            element.text = self.owner_id
        if self.docs is not None:
            element = XmlBuilder.SubElement(head, "docs")
            element.text = self.docs
        if self.expansion_state is not None:
            element = XmlBuilder.SubElement(head, "expansionState")
            element.text = self.expansion_state
        if self.vert_scroll_state is not None:
            element = XmlBuilder.SubElement(head, "vertScrollState")
            element.text = str(self.vert_scroll_state)
        if self.window_top is not None:
            element = XmlBuilder.SubElement(head, "windowTop")
            element.text = str(self.window_top)
        if self.window_left is not None:
            element = XmlBuilder.SubElement(head, "windowLeft")
            element.text = str(self.window_left)
        if self.window_bottom is not None:
            element = XmlBuilder.SubElement(head, "windowBottom")
            element.text = str(self.window_bottom)
        if self.window_right is not None:
            element = XmlBuilder.SubElement(head, "windowRight")
            element.text = str(self.window_right)

    def to_json(self) -> str:
        """Output the Head as a JSON string."""

        return json.dumps(
            self,
            default=lambda o: _dict_exclude_none(o.__dict__),
            indent=2,
            sort_keys=True,
        )
