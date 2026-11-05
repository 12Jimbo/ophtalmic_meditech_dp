Master: `.claude\context_grid\context_node_master.md` (last master commit: `2026-10-16T14:20:17Z`).

# Code Node Table (CNT)

| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sources\TED\semantic base\field semantics\web scrape\scrape_business_terms.py` | Exports TED business terms with separate business-group ID and name paths to CSV. | none |  | [`sources\TED\semantic base\eForm Metadata Reference.md`] | [`sources\TED\semantic base\field semantics\web scrape\business_terms.csv`] | `2026-11-05T16:46:27+01:00` | 3 |

| `sources\TED\semantic base\field semantics\web scrape\scrape_codelists.py` | Exports TED codelist metadata and code labels from the index and detail pages. | none |  | [`sources\TED\semantic base\eForm Metadata Reference.md`] | [`sources\TED\semantic base\field semantics\web scrape\codelists.csv`, `sources\TED\semantic base\field semantics\web scrape\codelist_codes.csv`] | `2026-11-05T17:02:24+01:00` | 1 |

# Data Node Table (DNT)

| resource | writers | readers | type | endpoint |
| --- | --- | --- | --- | --- |
| `sources\TED\semantic base\field semantics\web scrape\business_terms.csv` | [`sources\TED\semantic base\field semantics\web scrape\scrape_business_terms.py`] |  | table | self |
| `sources\TED\semantic base\field semantics\web scrape\codelists.csv` | [`sources\TED\semantic base\field semantics\web scrape\scrape_codelists.py`] |  | table | self |
| `sources\TED\semantic base\field semantics\web scrape\codelist_codes.csv` | [`sources\TED\semantic base\field semantics\web scrape\scrape_codelists.py`] |  | table | self |
