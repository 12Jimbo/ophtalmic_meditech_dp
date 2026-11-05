"""Export the TED Business Terms reference tables using only the standard library."""

import csv
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen


SOURCE_URL = "https://docs.ted.europa.eu/eforms/latest/reference/business-terms/index.html"
OUTPUT_PATH = Path(__file__).with_name("business_terms.csv")
COLUMNS = ["business_group_id", "business_group_name", "business_term_identifier", "Description", "Data Type"]


# Capture headings and table cells in document order, retaining nested group paths.
class BusinessTermsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.groups = {}
        self.heading = None
        self.cell = None
        self.cells = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h2", "h3", "h4", "h5", "h6"):
            self.heading = (int(tag[1]), [])
        elif tag == "tr":
            self.cells = []
        elif tag in ("td", "th"):
            self.cell = []

    def handle_data(self, data):
        if self.heading is not None:
            self.heading[1].append(data)
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if self.heading is not None and tag == f"h{self.heading[0]}":
            level, parts = self.heading
            title = " ".join("".join(parts).split())
            self.groups = {key: value for key, value in self.groups.items() if key < level}
            if title.startswith("BG-") or title == "Other":
                group_id, separator, group_name = title.partition(":")
                self.groups[level] = (group_id.strip(), group_name.strip()) if separator else ("", title)
            self.heading = None
        elif tag in ("td", "th") and self.cell is not None:
            self.cells.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.cells:
            identifier = self.cells[0]
            if identifier.startswith(("BT-", "OPT-", "OPP-", "OPA-")):
                if len(self.cells) != 4 or not self.groups:
                    raise ValueError(f"Unexpected business-term row: {self.cells}")
                groups = [self.groups[key] for key in sorted(self.groups)]
                group_ids = " > ".join(group_id for group_id, _ in groups)
                group_names = " > ".join(group_name for _, group_name in groups)
                self.rows.append(dict(zip(COLUMNS, [group_ids, group_names, *self.cells[:3]])))


# Validate the complete extraction before replacing the CSV.
def main():
    with urlopen(SOURCE_URL, timeout=60) as response:
        html = response.read().decode("utf-8")
    parser = BusinessTermsParser()
    parser.feed(html)
    parser.close()
    identifiers = [row["business_term_identifier"] for row in parser.rows]
    if not identifiers or len(identifiers) != len(set(identifiers)):
        raise ValueError("No business terms found, or duplicate identifiers encountered")
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(parser.rows)
    print(f"Saved {len(parser.rows)} business terms to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
