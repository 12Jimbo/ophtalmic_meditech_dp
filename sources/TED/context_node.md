Master: `.claude\context_grid\context_node_master.md` (last master commit: `2026-10-16T14:20:17Z`).

# Code Node Table (CNT)

| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sources\TED\ted explorer.ipynb` | Explores the public TED Search API with a JSON POST helper and sample date, Italian buyer, and ophthalmology queries. | none | none | none | none | `2026-10-16T15:00:39+02:00` | 3 |
| `sources\TED\onthology_mapper.ipynb` | Builds a prefix hierarchy and flat shared suffix groups for TED search fields; verifies coverage and reports excluded fields. | none |  | [`sources\TED\List_of_search_fields.csv`] | none | `2026-10-30T17:31:36+01:00` | 3 |

# Data Node Table (DNT)

| resource | writers | readers | type | endpoint |
| --- | --- | --- | --- | --- |
| `sources\TED\List_of_search_fields.csv` |  | [`sources\TED\onthology_mapper.ipynb`] |  |  |
