# TED Sourced Semantics


# [eForm Metadata Reference](https://docs.ted.europa.eu/eforms/latest/reference/index.html):

The resources below correspond to eForms SDK 1.15. The `latest` links may point to a newer version in the future; patch-version changes are not reflected in the reference documentation.

## Downloadable CSVs

### Nodes, fields, and notice subtypes

- [Nodes](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/nodes.csv): notice XML containers, their hierarchy, paths, and repeatability.
- [Fields](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/fields.csv): implementing fields for business terms, with descriptions, types, scope, and XML paths.
- [Notice subtypes](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/notices.csv): notice subtype IDs, descriptions, legal bases, and form/notice types.

### Business rules

- [All business rules](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/business-rules.csv): field-validation rules across notice subtypes, with applicability, severity, and EFX expressions.
- [Forbidden](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/forbidden-rules.csv): field-validation rules specifying when fields are not allowed.
- [Mandatory](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/mandatory-rules.csv): field-validation rules specifying when fields are required.
- [Codelist](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/codelist-rules.csv): field-validation rules linking fields to permitted codelists; code meanings are documented on the Codelists webpage.
- [Pattern](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/pattern-rules.csv): field-validation rules identifying required text patterns; regex definitions appear on the Business Rules webpage.
- [Interval](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/interval-rules.csv): field-validation rules identifying permitted numeric intervals; explicit bounds appear on the Business Rules webpage.
- [Co-constraints](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/coconstraint-rules.csv): field-validation rules expressing dependencies between fields.
- [Repeatability](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/repeatability-rules.csv): field-validation rules limiting repeated field occurrences.
- [Changeability](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/changeability-rules.csv): field-validation rules restricting changes between notice versions.
- [Lawfulness](https://docs.ted.europa.eu/eforms/latest/reference/_attachments/lawfulness-rules.csv): field-validation rules checking publication eligibility.

## Webpages

- [Business Terms](https://docs.ted.europa.eu/eforms/latest/reference/business-terms/index.html): business terms grouped by business group, with term-level types and links to implementing fields in the Fields CSV.
- [Business Rules](https://docs.ted.europa.eu/eforms/latest/reference/business-rules/index.html): field-validation rules across notice subtypes, with applicability, severity, regex definitions, and numeric interval bounds; complements the business-rule CSVs.
- [Codelists](https://docs.ted.europa.eu/eforms/latest/reference/code-lists/index.html): permitted codelists and code meanings, with versions, field usage, and relationships; complements the Codelist rules CSV.

# Findings

## Business terms and fields

[fields.csv](field%20semantics/CSVs%20download/fields.csv) describes implementing fields, linked to business terms through `btId`. The Business Terms webpage adds business-group IDs, names, nesting, and term-level types. The CSV adds field descriptions, types, scope, XML paths, length, and privacy metadata.

Types describe different levels, so neither source is a strict superset:

| Business term | Webpage type | Implementing field types |
| --- | --- | --- |
| Title (BT-21) | TEXT | text-multilingual; code for language |
| Estimated Value (BT-27) | VALUE | amount; code for currency |
| Duration Period (BT-36) | DURATION | measure; code for unit; associated number fields |

These examples show decomposition, not contradictions; type consistency was not exhaustively audited. Linked term pages repeat term types and list implementing fields. On 2026-11-05, 30 of the 387 scraped term identifiers had no matching `btId` in the saved 1,256-row Fields CSV; the cause is unresolved.

## Combined and specific business-rule CSVs

All 27,848 records across the nine specific rule CSVs match `(ruleId, fieldId, noticeSubtype)` keys in [business-rules.csv](field%20rules/CSVs%20download/business-rules.csv), as checked on 2026-11-05. **Keep both:** matching keys do not mean identical metadata.

| Specific CSV | Additional populated column absent from the combined CSV |
| --- | --- |
| changeability-rules.csv | canModify |
| coconstraint-rules.csv | contextNode |
| codelist-rules.csv | codeListParentId |
| interval-rules.csv | intervalId |

Specific CSVs also provide human-readable `description`, `condition`, and `expression`; the combined CSV uses labels and EFX expressions. These representations are not interchangeable.

## Business Rules webpage and rule CSVs

The webpage presents the same field-validation rules, but resolves definitions referenced by the CSVs:

- Pattern rule `BR-BT-00031-0075`: `Integer` becomes regex `^([0-9]+)$`.
- Interval rule `BR-BT-00031-0076`: `ZeroToTenThousand` becomes explicit bounds `0 - 9999`; the specific CSV description only states less than 10,000.

These are checked examples, not an exhaustive comparison. [business_rules_universal.csv](field%20rules/web%20scrape/business_rules_universal.csv) captures the universal tables with their rule types. Subtype-specific tables remain unscraped.

## Codelists and code meanings

A **codelist** is a controlled vocabulary of codes and meanings. For example, `framework-agreement` defines `fa-w-rc` as a framework agreement with reopening of competition. A codelist rule links a field to its permitted vocabulary; a tailored codelist restricts a broader vocabulary to a particular use.

Rule CSVs store field-to-codelist references and applicability. The Codelists webpage adds vocabulary metadata and code meanings, exported locally as:

- [codelists.csv](field%20semantics/web%20scrape/codelists.csv): descriptions, categories, versions, relationships, vocabulary links, and business-term usage. Multiple category memberships share one record.
- [codelist_codes.csv](field%20semantics/web%20scrape/codelist_codes.csv): codes and English labels, linked through `codelist_id`; external multilingual labels are not included.

Codelists explain coded values, such as currency (`cur`), once API fields are mapped to eForms fields and rules. API mappings and field metadata remain necessary for scope suffixes (`proc`, `lot`, `part`) and representation suffixes (`i18ns`).

## Project modelling decisions

Prioritize business groups for semantic organization and API structure, identifiers, scope, and cardinalities for record relationships. A business group need not become a database entity: its terms can apply at procedure, lot, or other scopes.

XML nodes describe structural containers, not necessarily business entities. Their relevance is secondary for this API-based workflow. The local `nodes.csv` was removed; retain the download link above for cases where XML structure helps clarify relationships.
