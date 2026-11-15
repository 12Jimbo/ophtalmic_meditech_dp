# EUDAMED semantic base

[semantic_base.csv](semantic_base.csv) keeps request parameters and observed response fields together. [field_values.csv](field_values.csv) records values with their evidence and representation. [semantic_base_metadata.csv](semantic_base_metadata.csv) defines both schemas, their sources, nullability and controlled vocabularies.

## Row identity and mappings

The semantic map has one row per endpoint and field concept. Its key is `endpoint` plus `response_field` when present, otherwise `request_field`. Exact same-named request and response fields within an endpoint share a row. Fields seen on only one side retain a blank on the other side. `request_location` distinguishes headers from query parameters.

`description` is shared between request and response. `data_dictionary` and `data_dictionary_field` record one reviewed candidate, while `mapping_evidence` explains its scope and any subtype-specific alternatives. A selected dictionary candidate is not a universal field identity: for example, regulatory and legacy identifiers use different dictionary records. Composite exports such as `MULTI_COMPONENT_ID` retain their alternatives in evidence without forcing a single dictionary field. Source paths in both CSVs and schema metadata are relative to `sources/EUDAMED/`; `#pdf-page=` uses physical PDF pages, including cover pages. Metadata `data_type` describes the logical value, while CSV is a text serialization.

| Status | Rule |
| --- | --- |
| `verified` | Official API documentation explicitly defines the API concept and the row has no unverified dictionary link. This does not establish exact filter matching behaviour. |
| `inferred` | Document definitions and current sample checks support a business meaning, dictionary candidate or projection, but do not establish every link explicitly. Missing dictionary linkage alone does not prevent a supported description. |
| `unresolved` | Identity, scope or contradictory evidence remains material. A qualified structural description can still be recorded; a populated description is not proof of a resolved mapping. |

The reviewed snapshot has 97 rows covering all 29 parameters in the original Swagger and all 89 response columns across the three samples: 80 inferred, 10 verified and 7 unresolved. All rows have descriptions, including qualified observations for unresolved technical fields. No dictionary link is marked verified based solely on a matching name.

The unresolved fields are `/udi` `ID`, `UUID`, `UDI_DI_DATA_ULID`, `BASIC_UDI_DATA_UUID`, `BASIC_UDI_DATA_ULID`, `LATEST_VERSION` and `STATUS_ID`. Identifier format and uniqueness in a sample do not establish entity/version scope, persistence or global keys. The registration infographics define UDI-DI, Basic UDI-DI and package UDI-DI; they do not identify these API technical columns. For `DIRECT_MARKETING_DI`, direct marking remains a candidate interpretation. The country-valued `PLACED_ON_THE_MARKET_ID` is not forced onto an EU-member-state-only dictionary field. No row requires splitting request and response tables.

## Review findings

- Legacy records: all 229 sampled `BASIC_UDI` values start with `B-`; 14 `PRIMARY_DI` values start with `D-`. The Legacy Devices guide and dictionary identify EUDAMED DI and EUDAMED ID as legacy alternatives. They must be distinguished from UUID/ULID and numeric export identifiers.
- Actor roles: the 18 SPP rows use `PR` SRNs in `MF_SRN`; the other 982 rows use `MF`. Manufacturer-prefixed fields therefore also carry SPP-producer information. The scalar actor identifier maps to `FLD-ACT-001`, with manufacturer/producer relationships explained separately. Competent-authority name/ID filters likewise use scalar candidates, with the responsible-authority relation retained in evidence.
- Multilingual names: all 1,000 populated `MF_ACTOR_NAMES` and all 479 populated `AR_ACTOR_NAMES` cells parse as JSON text and contain their corresponding scalar name. All 23 comparable manufacturer-actor abbreviation joins match. This supports the name projections, but not a universal language-selection rule or native API JSON type.
- SPP medical purpose: exactly 18 rows are populated, all SPP. `FLD-UDID-260` in the Basic UDI SPP dictionary supplies the missing definition. A multilingual dictionary field can have a scalar CSV projection.
- Versions: scalar `VERSION` and `VERSION_NUMBER` use `VersionData`'s `FLD-EUD-013` candidate, rather than incorrectly mapping only to a parent version relation. `LATEST_VERSION` remains unresolved because every sampled value is `1`.
- Substance and activity flags: substance-presence concepts are supported by the device guide, but a substance list is not the same field as a scalar flag. Missing is not false. `ACTIVE` describes an active-device design characteristic; `STATUS_ID` labels indicate active/inactive but their exact lifecycle scope is unresolved. Neither is the market-status field `DEVICE_STATUS_TYPE_ID`.
- Multiple-value exports: 12 populated EMDN cells and all 56 populated container-package cells contain commas in this snapshot. Their complete cell values remain observations; they are not treated as individual allowed codes. The fourth multi-component dictionary value, `SPP_PROCEDURE_PACK`, continues onto PDF page 17 and is now included.

The review searched 13 relevant PDF snapshots (362 pages): both registration infographics, the Public API/UDI Devices/Legacy Devices/Public site/Economic Operators guides, and the Common/ACT/UDI business rules and enumerations. Both infographics were visually inspected. Dictionary candidates were checked in ACT, Common, Basic UDI, UDI-DI, Basic UDI SPP and Legacy Devices CSVs. This is a source review, not a fresh live API test.

## Value evidence

Join the catalogue using `endpoint` and `field` against the semantic map's canonical field key above. All values, including numeric IDs and identifiers with leading zeros, are stored as strings.

- `observed`: distinct nonempty values in a local response sample. These do not define allowed values. Literal `NULL` sample markers are excluded. List-like values remain whole export strings; they are not interpreted as atomic enum members.
- `reference-listed`: API IDs with source labels and languages, or codes in the local EMDN catalogue. API IDs are qualified by category (`CODE`) and language. A code appearing in EMDN does not prove that the API accepts every classification level.
- `allowed`: values explicitly listed in Swagger or a reviewed official PDF. Always check `value_scope`: `request`, `response`, `request_response` or `dictionary`. Dictionary-only submission codes are not API IDs or verified API inputs.

The three API samples each contain 1,000 rows. The reference sample covers seven categories and is incomplete. Unlabelled observed IDs remain unlabelled where the reference sample has no match. English is not substituted for missing labels in another language. `source_date` is blank for these undated snapshots; the build date and filesystem timestamps are not extraction dates.

The current UDI sample contains 54 distinct ID/category pairs across those seven categories. Two lack labels in the reference sample: `RISK_CLASS_ID=-203` and `SPECIAL_DEVICE_TYPE_ID=-1202`. The value catalogue has 33,596 evidence rows; its coverage remains incomplete.

The current catalogue includes the full local EMDN 2026 table, all sample observations and reference rows, Swagger format options, the API guide's actor-type options, and selected ACT/UDI enumeration lists. It is not an exhaustive transcription of all enumeration PDFs. Some PDF enum text is garbled, and unverified translations between dictionary codes and API IDs remain absent. Actor-status and actor-type codes in PDFs differ in spelling/case from sample labels. The workflow enum is not assigned to `STATUS_ID`.

## Source differences to retain

The Public API guide says JSON only, whereas the Swagger lists JSON and CSV. It describes batches of 100 rows, whereas the retained exploration notes report 1,000; no fresh API pagination test was performed. It also calls numeric reference parameters strings and contains parameter-name typos (`PRIMARY_UDI`, `placecd_on_the_market_id`). Exact request names come from Swagger. The guide documents `api-version`, which is absent from Swagger and is therefore not added to the request-field inventory.

Descriptions and values do not establish table grain, primary keys, cardinalities or a complete response schema. Those require separate modelling checks.

## Sources and rebuilding

- [User guides](user%20guides/README.md): API-specific definitions, reference lookup instructions and selected documented values.
- [Technical documentation](technical%20documentation/README.md): candidate dictionary definitions, enumeration references and submission value lists.
- [Device registration guides](device%20registration%20guides/README.md): identifier concepts and device categories.
- [Exploration findings](../findings.md): historical observations and interpretations requiring validation.

Run `python "sources/EUDAMED/semantic base/semantic_base_builder.py"` from the project root to regenerate the three EUDAMED CSVs using only Python's standard library. Paths are relative to the script, so it also works from other directories. Curated dictionary candidates and PDF lists are explicit in the builder; changing a PDF requires reviewing that curation. Context nodes record the builder's runtime file reads and writes. Manually consulted PDFs remain cited in output provenance and are not represented as runtime PDF reader edges. The builder validates endpoint/field coverage and value foreign keys before writing.

For the existing TED map, see [semantic_base_metadata.csv](../../TED/semantic%20base/semantic_base_metadata.csv). TED's existing grain is a search field plus a parsed SDK reference, so its multiple rows per search field are intentional. Its builder now produces its schema metadata alongside the unchanged semantic map. Swagger enrichment is deferred.
