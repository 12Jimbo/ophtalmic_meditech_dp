Master: `.claude\context_grid\context_node_master.md` (last master commit: `2026-10-16T14:20:17Z`).

# Code Node Table (CNT)

| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sources\TED\semantic base\API map\onthology_mapper.ipynb` | Builds lexical prefix and suffix maps; checks BT row/null counts, key overlap and left/right join row counts with pandas merge. | none |  | [`sources\TED\semantic base\API map\List_of_search_fields.csv`, `sources\TED\semantic base\field semantics\web scrape\codelists.csv`, `sources\TED\semantic base\field semantics\web scrape\business_terms.csv`] | none | `2026-11-06T16:56:48+01:00` | 16 |


# Data Node Table (DNT)

| resource | writers | readers | type | endpoint |
| --- | --- | --- | --- | --- |
| `sources\TED\semantic base\API map\List_of_search_fields.csv` |  | [`sources\TED\semantic base\API map\onthology_mapper.ipynb`, `sources\TED\semantic base\semantic_base_exploration.ipynb`, `sources\TED\semantic base\semantic_base_builder.py`] | table | self |
