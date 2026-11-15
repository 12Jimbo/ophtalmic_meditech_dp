Master: `.claude\context_grid\context_node_master.md` (last master commit: `2026-10-16T14:20:17Z`).

# Code Node Table (CNT)

| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |

| `sources\TED\semantic base\semantic_base_builder.py` | Builds the TED search-field to SDK map and its schema metadata from local source CSVs. | none | [`sources\TED\semantic base\semantic_base_exploration.ipynb`] | [`sources\TED\semantic base\API\List_of_search_fields.csv`, `sources\TED\semantic base\field semantics\CSVs download\fields.csv`] | [`sources\TED\semantic base\semantic_base.csv`, `sources\TED\semantic base\semantic_base_metadata.csv`] | `2026-11-15T17:18:23+01:00` | 5 |

| `sources\TED\semantic base\semantic_base_exploration.ipynb` | Explores hierarchies and semantic relationships, reusing loaded dataframes for diagnostics and the shared builder join. | [`sources\TED\semantic base\semantic_base_builder.py`] |  | [`sources\TED\semantic base\API\List_of_search_fields.csv`, `sources\TED\semantic base\field semantics\web scrape\codelists.csv`, `sources\TED\semantic base\field semantics\web scrape\business_terms.csv`, `sources\TED\semantic base\field semantics\CSVs download\fields.csv`, `sources\TED\semantic base\field semantics\web scrape\codelist_codes.csv`] | none | `2026-11-15T11:28:55+01:00` | 7 |

# Data Node Table (DNT)

| resource | writers | readers | type | endpoint |
| --- | --- | --- | --- | --- |
| `sources\TED\semantic base\eForm Metadata Reference.md` |  | [`sources\TED\semantic base\field semantics\web scrape\scrape_business_terms.py`, `sources\TED\semantic base\field rules\web scrape\scrape_business_rules.py`, `sources\TED\semantic base\field semantics\web scrape\scrape_codelists.py`] | API | https://docs.ted.europa.eu/eforms/latest/reference/index.html |
| `sources\TED\semantic base\notices.csv` |  |  | table | self |
| `sources\TED\semantic base\semantic_base.csv` | [`sources\TED\semantic base\semantic_base_builder.py`] |  | table | self |
| `sources\TED\semantic base\semantic_base_metadata.csv` | [`sources\TED\semantic base\semantic_base_builder.py`] |  | table | self |
