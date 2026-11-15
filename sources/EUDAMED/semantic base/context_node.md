Master: `.claude/context_grid/context_node_master.md` (last master commit: `2026-10-16T14:20:17Z`).

# Code Node Table (CNT)

| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |

| `sources/EUDAMED/semantic base/semantic_base_builder.py` | Builds unified API field descriptions, evidence, value catalogue and schema metadata from local EUDAMED snapshots. | none | none | [`sources/EUDAMED/semantic base/user guides/data exchange/swagger.yaml`, `sources/EUDAMED/semantic base/technical documentation/data dictionaries/EMDN/EMDN v2026_EN.csv`, `sources/EUDAMED/data samples/eudamed api actors.csv`, `sources/EUDAMED/data samples/eudamed api reference.csv`, `sources/EUDAMED/data samples/eudamed api udi.csv`, `sources/EUDAMED/semantic base/technical documentation/data dictionaries/ACT/ACT - data dictionary-Actor.csv`, `sources/EUDAMED/semantic base/technical documentation/data dictionaries/EUD Common/EUD - data dictionary-Common Entities.csv`, `sources/EUDAMED/semantic base/technical documentation/data dictionaries/UID Devices/UDI Devices - data dictionary-DD BASIC UDI.csv`, `sources/EUDAMED/semantic base/technical documentation/data dictionaries/UID Devices/UDI Devices - data dictionary-DD UDI-DI.csv`, `sources/EUDAMED/semantic base/technical documentation/data dictionaries/UID Devices/UDI Devices - data dictionary-DD BASIC UDI_SPP.csv`, `sources/EUDAMED/semantic base/technical documentation/data dictionaries/UID Devices/UDI Devices - data dictionary-DD Legacy Devices.csv`] | [`sources/EUDAMED/semantic base/semantic_base.csv`, `sources/EUDAMED/semantic base/field_values.csv`, `sources/EUDAMED/semantic base/semantic_base_metadata.csv`] | `2026-11-15T17:18:23+01:00` | 3 |

# Data Node Table (DNT)

| resource | writers | readers | type | endpoint |
| --- | --- | --- | --- | --- |
| `sources/EUDAMED/semantic base/semantic_base.csv` | [`sources/EUDAMED/semantic base/semantic_base_builder.py`] | | table | self |
| `sources/EUDAMED/semantic base/field_values.csv` | [`sources/EUDAMED/semantic base/semantic_base_builder.py`] | | table | self |
| `sources/EUDAMED/semantic base/semantic_base_metadata.csv` | [`sources/EUDAMED/semantic base/semantic_base_builder.py`] | | table | self |
