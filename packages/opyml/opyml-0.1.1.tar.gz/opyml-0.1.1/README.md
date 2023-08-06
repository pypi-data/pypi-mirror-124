# opyml

An OPML library for Python.

This is a largely identical "port" of [the Rust crate](https://github.com/Holllo/opml).

## Example

```python
from opyml import OPML, Outline

# Create OPML documents from scratch.
document = OPML()
document.body.outlines.append(Outline(text="Example"))

# Convert documents to XML.
xml = document.to_xml()

# Parse OPML documents from XML.
document = OPML.from_xml(xml)
```

For complete examples check out the `tests/` directory.

## Development

* Install dependencies with [Poetry](https://python-poetry.org) (`poetry shell` + `poetry install`).
* Format code with `black opyml tests`.
* Check types with `mypy opyml`.
* Run tests and collect coverage with `pytest --cov=opyml --cov-report html`.
* Generate documentation with `pdoc opyml`.

## License

Dual-licensed with the [Apache License, Version 2.0](https://github.com/Holllo/opyml/blob/main/LICENSE-Apache) and [MIT license](https://github.com/Holllo/opyml/blob/main/LICENSE-MIT).
