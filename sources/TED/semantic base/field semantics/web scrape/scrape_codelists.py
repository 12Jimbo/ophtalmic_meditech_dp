"""Export TED codelist metadata and code labels alongside this script.

Run with Python; only the standard library is required. Both CSVs are replaced
only after every detail page has been fetched and validated.
"""

import csv
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen

SOURCE_URL = "https://docs.ted.europa.eu/eforms/latest/reference/code-lists/index.html"
OUTPUT_DIR = Path(__file__).parent
METADATA_COLUMNS = [
    "codelist_id", "category", "description", "version", "subset_of",
    "tailored_by", "uri", "structure", "eu_vocabularies_url", "used_in", "source_url",
]
CODE_COLUMNS = ["codelist_id", "code", "label"]


# Reduce the article HTML to ordered headings, paragraphs, links, and table rows.
class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.capture = None
        self.parts = []
        self.links = []
        self.cells = []
        self.events = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article" and "doc" in attrs.get("class", "").split():
            self.active = True
        if not self.active:
            return
        if tag == "tr":
            self.cells = []
        if tag in ("td", "th", "h2", "h3") or (tag == "p" and self.capture is None):
            self.capture, self.parts, self.links = tag, [], []
        if tag == "a":
            href = attrs.get("href", "")
            if self.capture:
                self.links.append(href)
            self.events.append(("link", href, []))

    def handle_data(self, data):
        if self.active and self.capture:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "article":
            self.active = False
        if not self.active:
            return
        if tag == self.capture:
            text = " ".join("".join(self.parts).split())
            if tag in ("td", "th"):
                self.cells.append((text, self.links))
            else:
                self.events.append((tag, text, self.links))
            self.capture = None
        if tag == "tr":
            self.events.append(("row", self.cells, []))


def fetch(url):
    with urlopen(url, timeout=60) as response:
        html = response.read().decode("utf-8")
    parser = ArticleParser()
    parser.feed(html)
    parser.close()
    return parser.events


# The index establishes list identity, category, descriptions, and relationships.
def read_index(events):
    records = []
    category = ""
    current = None
    for kind, value, links in events:
        if kind == "h2":
            category = value
        elif kind == "h3":
            current = dict.fromkeys(METADATA_COLUMNS, "")
            current.update(codelist_id=value, category=category)
            records.append(current)
        elif current is not None:
            if kind == "p" and not current["description"]:
                current["description"] = value
            elif kind == "row" and len(value) == 2:
                key = value[0][0].lower().replace(" ", "_")
                if key in ("version", "subset_of", "tailored_by"):
                    current[key] = value[1][0]
            elif kind == "link" and value.endswith(".html") and not value.startswith("#"):
                # Detail links share the codelist identifier as their filename.
                if value.rsplit("/", 1)[-1] == current["codelist_id"] + ".html":
                    current["source_url"] = urljoin(SOURCE_URL, value)
    if not records or any(not r["source_url"] for r in records):
        raise ValueError("Missing codelists or detail-page links in index")
    # Some lists appear in both the tailored and technical sections.
    unique = {}
    for record in records:
        identifier = record["codelist_id"]
        if identifier not in unique:
            unique[identifier] = record
            continue
        existing = unique[identifier]
        categories = existing["category"].split(" | ")
        if record["category"] not in categories:
            existing["category"] += " | " + record["category"]
        for column in METADATA_COLUMNS:
            if column != "category" and record[column]:
                if existing[column] and existing[column] != record[column]:
                    raise ValueError(f"Conflicting {column} for {identifier}")
                existing[column] = record[column]
    return list(unique.values())


# Detail pages resolve each list into its vocabulary metadata and code labels.
def read_detail(record):
    codes = []
    in_codes = False
    for kind, value, links in fetch(record["source_url"]):
        if kind == "h2":
            in_codes = value == "Codes"
        elif kind == "row" and len(value) == 2:
            (key, _), (text, cell_links) = value
            if in_codes:
                codes.append(dict(zip(CODE_COLUMNS, [record["codelist_id"], key, text])))
            else:
                column = key.lower().replace(" ", "_")
                if column in record:
                    record[column] = text
                elif key == "EU Vocabularies" and cell_links:
                    record["eu_vocabularies_url"] = urljoin(record["source_url"], cell_links[0])
    if not codes or any(not row["code"] or not row["label"] for row in codes):
        raise ValueError(f"Missing codes or labels for {record['codelist_id']}")
    return record, codes


def write_csv(filename, rows, columns):
    with (OUTPUT_DIR / filename).open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


# Limit concurrent requests and preserve index order in both exports.
def main():
    records = read_index(fetch(SOURCE_URL))
    print(f"Fetching {len(records)} codelist detail pages...", flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(read_detail, records))
    metadata = [record for record, _ in results]
    codes = [code for _, rows in results for code in rows]
    keys = [(row["codelist_id"], row["code"]) for row in codes]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate codes within a codelist")
    write_csv("codelists.csv", metadata, METADATA_COLUMNS)
    write_csv("codelist_codes.csv", codes, CODE_COLUMNS)
    print(f"Saved {len(metadata)} codelists and {len(codes)} codes.")


if __name__ == "__main__":
    main()
