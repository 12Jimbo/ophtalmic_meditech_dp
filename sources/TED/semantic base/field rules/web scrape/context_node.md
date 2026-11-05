Master: `.claude\context_grid\context_node_master.md` (last master commit: `2026-10-16T14:20:17Z`).

# Code Node Table (CNT)

| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sources\TED\semantic base\field rules\web scrape\scrape_business_rules.py` | Exports universal TED rules; optional --notice-subtype ID exports selected subtype-specific tables. | none |  | [`sources\TED\semantic base\eForm Metadata Reference.md`] | [`sources\TED\semantic base\field rules\web scrape\business_rules_universal.csv`, `sources\TED\semantic base\field rules\web scrape\business_rules_specific.csv`] | `2026-11-05T16:46:27+01:00` | 2 |

# Data Node Table (DNT)

| resource | writers | readers | type | endpoint |
| --- | --- | --- | --- | --- |
| `sources\TED\semantic base\field rules\web scrape\business_rules_universal.csv` | [`sources\TED\semantic base\field rules\web scrape\scrape_business_rules.py`] |  | table | self |
| `sources\TED\semantic base\field rules\web scrape\business_rules_specific.csv` | [`sources\TED\semantic base\field rules\web scrape\scrape_business_rules.py`] |  | table | self |
