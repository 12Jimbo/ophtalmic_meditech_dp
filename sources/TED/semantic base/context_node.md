Master: `.claude\context_grid\context_node_master.md` (last master commit: `2026-10-16T14:20:17Z`).

# Code Node Table (CNT)

| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |

| `sources\TED\semantic base\semantic_base_builder.py` | Builds semantic_base.csv with expanded API references and SDK metadata, retaining the normalized SDK key instead of fieldId. | none | [`sources\TED\semantic base\semantic_base_exploration.ipynb`] | [`sources\TED\semantic base\API map\List_of_search_fields.csv`, `sources\TED\semantic base\field semantics\CSVs download\fields.csv`] | [`sources\TED\semantic base\semantic_base.csv`] | `2026-11-07T17:59:44+01:00` | 2 |

| `sources\TED\semantic base\semantic_base_exploration.ipynb` | Explores search-field hierarchies, semantic relationships, and SDK metadata joined through the shared semantic-base builder. | [`sources\TED\semantic base\semantic_base_builder.py`] |  | [`sources\TED\semantic base\API map\List_of_search_fields.csv`, `sources\TED\semantic base\field semantics\web scrape\codelists.csv`, `sources\TED\semantic base\field semantics\web scrape\business_terms.csv`, `sources\TED\semantic base\field semantics\CSVs download\fields.csv`, `sources\TED\semantic base\field semantics\web scrape\codelist_codes.csv`] | none | `2026-11-07T18:39:53+01:00` | 5 |

# Data Node Table (DNT)

| resource | writers | readers | type | endpoint |
| --- | --- | --- | --- | --- |
| `sources\TED\semantic base\eForm Metadata Reference.md` |  | [`sources\TED\semantic base\field semantics\web scrape\scrape_business_terms.py`, `sources\TED\semantic base\field rules\web scrape\scrape_business_rules.py`, `sources\TED\semantic base\field semantics\web scrape\scrape_codelists.py`] | API | https://docs.ted.europa.eu/eforms/latest/reference/index.html |
| `sources\TED\semantic base\notices.csv` |  |  | table | self |
| `sources\TED\semantic base\semantic_base.csv` | [`sources\TED\semantic base\semantic_base_builder.py`] |  | table | self |
