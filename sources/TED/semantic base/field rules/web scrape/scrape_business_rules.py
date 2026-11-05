"""Export universal rules by default; use --notice-subtype 1 for subtype-only rules.

Run from the project root:
    .venv/Scripts/python.exe "sources/TED/semantic base/field rules/web scrape/scrape_business_rules.py"
Repeat --notice-subtype to select multiple subtypes. Subtype exports do not include
universal rules, which remain in business_rules_universal.csv.
"""

import argparse
import csv
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen


SOURCE_URL = "https://docs.ted.europa.eu/eforms/latest/reference/business-rules/index.html"
OUTPUT_DIR = Path(__file__).parent
COLUMNS = ["rule_type", "Business Rule", "Field", "Details", "Severity"]


# Read table rows under their rule-type headings and discover subtype links.
class BusinessRulesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.heading = None
        self.rule_type = None
        self.cell = None
        self.cells = []
        self.rows = []
        self.subtype_urls = {}

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a":
            href = attributes.get("href", "")
            filename = href.rsplit("/", 1)[-1]
            if filename.startswith("notice-subtype-") and filename.endswith(".html"):
                subtype = filename.removeprefix("notice-subtype-").removesuffix(".html")
                self.subtype_urls[subtype] = urljoin(SOURCE_URL, href)
        if tag in ("h2", "h3"):
            self.heading = (tag, [])
            if tag == "h2":
                self.rule_type = None
        elif tag == "tr":
            self.cells = []
        elif tag in ("td", "th"):
            self.cell = []
        elif self.cell is not None and tag in ("p", "pre", "br"):
            self.cell.append("\n")

    def handle_data(self, data):
        if self.heading is not None:
            self.heading[1].append(data)
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if self.heading is not None and tag == self.heading[0]:
            if tag == "h3":
                self.rule_type = " ".join("".join(self.heading[1]).split())
            self.heading = None
        elif tag in ("td", "th") and self.cell is not None:
            lines = (line.strip() for line in "".join(self.cell).splitlines())
            self.cells.append("\n".join(line for line in lines if line))
            self.cell = None
        elif tag == "tr" and self.cells and self.cells[0].startswith("BR-"):
            if len(self.cells) != 4 or not self.rule_type:
                raise ValueError(f"Unexpected rule row: {self.cells}")
            self.rows.append(dict(zip(COLUMNS, [self.rule_type, *self.cells])))


# Share fetching and validation between universal and optional subtype exports.
def scrape_page(url):
    with urlopen(url, timeout=60) as response:
        html = response.read().decode("utf-8")
    parser = BusinessRulesParser()
    parser.feed(html)
    parser.close()
    keys = [(row["rule_type"], row["Business Rule"], row["Field"]) for row in parser.rows]
    if not keys or len(keys) != len(set(keys)):
        raise ValueError(f"Missing or duplicate rule records at {url}")
    return parser


def write_csv(path, rows, columns):
    with path.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rules to {path}")


# Subtype pages are requested only when explicitly selected on the command line.
def main():
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("--notice-subtype", action="append", default=[], metavar="ID")
    args = arguments.parse_args()
    index = scrape_page(SOURCE_URL)
    if not args.notice_subtype:
        write_csv(OUTPUT_DIR / "business_rules_universal.csv", index.rows, COLUMNS)
        return
    subtypes = list(dict.fromkeys(args.notice_subtype))
    unknown = set(subtypes) - index.subtype_urls.keys()
    if unknown:
        arguments.error(f"Unknown notice subtype(s): {', '.join(sorted(unknown))}")
    rows = []
    for subtype in subtypes:
        page = scrape_page(index.subtype_urls[subtype])
        rows.extend({"notice_subtype": subtype, **row} for row in page.rows)
    write_csv(OUTPUT_DIR / "business_rules_specific.csv", rows, ["notice_subtype", *COLUMNS])


if __name__ == "__main__":
    main()
