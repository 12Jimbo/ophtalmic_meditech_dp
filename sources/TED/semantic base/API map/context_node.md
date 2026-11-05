Master: `.claude\context_grid\context_node_master.md` (last master commit: `2026-10-16T14:20:17Z`).

# Code Node Table (CNT)

| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sources\TED\semantic base\API map\onthology_mapper.ipynb` | Builds a lexical prefix hierarchy and shared suffix groups; verifies field coverage. | none |  | [`sources\TED\semantic base\API map\List_of_search_fields.csv`] | none | `2026-11-05T16:46:27+01:00` | 5 |

# Data Node Table (DNT)

| resource | writers | readers | type | endpoint |
| --- | --- | --- | --- | --- |
| `sources\TED\semantic base\API map\List_of_search_fields.csv` |  | [`sources\TED\semantic base\API map\onthology_mapper.ipynb`] | table | self |
