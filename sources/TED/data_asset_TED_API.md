# TED API Search Request

## Project references
- **Swagger:** [swagger_TED-api-v3.yaml](./swagger_TED-api-v3.yaml) is a cleaned up version of the original swagger found at [API documentation](https://api.ted.europa.eu/swagger-ui/index.html#/Search/search). The present document includes API search request essentials, leaving out requested fields details.

- **Aliases Map:** [List_of_search_fields.csv](./List_of_search_fields.csv),  downoaded from [Search fields used on the TED website](https://docs.ted.europa.eu/ODS/latest/reuse/field-list.html), lists 1,340 unique primary names in `Search field`, alternative names in `Alias 1` and `Alias 2`, and references in `Reference in the eForms SDK`.

- **Semantic field map:** [semantic_base.json](./semantic_base.json), maps each of the 1,338 retained swagger search field names to a semantic description, initialized to an empty string (`""`). Note: the swagger's field descriptions explain multilingual text structure and language codes, rather than business meaning.

## Swagger Cleanup
The original swagger presented redundancies that have been eliminated to produce a project's version of the swagger:
1. Field duplicates: the list of fields for the search api body (section PublicExpertSearchRequestV1) included an example section that just relisted all the 1830 fields
2. Field aliases: using [List_of_search_fields.csv](./List_of_search_fields.csv). Removed 492 alias names in the original swagger from both `PublicExpertSearchRequestV1.properties.fields.enum` and `NoticeResponse.properties`, preferring the CSV's `Search field` name. Both sections now contain the same 1,338 unique names.

Notice that the CSV's `Search field` column and the edited swagger search request share 1,337 names but do not match exactly:

| Location | Names absent from the other list |
|---|---|
| CSV only | `buyer-country-i18ns`, `deletion-date`, `previous-planning-identifier` |
| Enum only | `links` |


## Search request

**Request URL**: https://api.ted.europa.eu/v3/notices/search

**HTTP method**: `POST`

**Request content type**: `application/json`

Request body of the notice search endpoint:

| Parameter | Type | Required | Default | Constraints / Allowed Values | Description |
|---|---|---|---|---|---|
| `query` | `string` | Yes | — | Minimum 1 character | Search query used to retrieve notices. |
| `fields` | `array<string>` | Yes | — | Minimum 1 item | Distinct fields to include in the search results; see the compact example below and the [full field definitions](./swagger_TED-api-v3.yaml). |
| `page` | `integer (int32)` | No | `1` | Minimum: `1` | Result page number, used to paginate results. |
| `limit` | `integer (int32)` | No | `10` | Minimum: `0`; maximum: 250 notices per page | Maximum number of notices returned per page. Up to 10,000 fields can be retrieved per page, calculated as `fields.length × limit`. |
| `scope` | `string` | No | `"ALL"` | `LATEST`, `ACTIVE`, `ALL` | Defines the search scope. `LATEST`: only notices from the current OJ S release. `ACTIVE`: only active notices. `ALL`: all notices. |
| `checkQuerySyntax` | `boolean` | No | `false` | `true`, `false` | When `true`, validates the query syntax without executing the search. |
| `paginationMode` | `string` | No | `"PAGE_NUMBER"` | `PAGE_NUMBER`, `ITERATION` | `PAGE_NUMBER`: standard pagination, supporting up to 15,000 notices per query. `ITERATION`: token-based pagination without a limit on total retrievable notices, but does not allow selecting a specific page. |
| `onlyLatestVersions` | `boolean` | No | `false` | `true`, `false` | When `true`, includes only the latest versions of notices. |
| `iterationNextToken` | `string` | No | — | Only applicable in `ITERATION` mode | Opaque token returned by the previous search request to retrieve the next result page. Must not be provided in `PAGE_NUMBER` mode or in the first `ITERATION` request. |

## Successful response (`200`)

| Field | Type | Description |
|---|---|---|
| `notices` | `array<object>` | Matching notices containing the requested fields. Individual fields may be scalars, arrays, or multilingual objects; their definitions are in `swagger_TED-api-v3.yaml`. |
| `totalNoticeCount` | `integer (int64)` | Total number of notices matching the query. |
| `iterationNextToken` | `string` | Token used to retrieve the next batch in `ITERATION` mode. |
| `timedOut` | `boolean` | Indicates whether the search timed out. |

## Request and response example

This request searches 2025 notices from Italian buyers for ophthalmology equipment (CPV `33122000`). The nine selected fields cover identifiers, dates, multilingual text, arrays, a monetary amount with its currency, and an integer limit on lots.

### Request body

```json
{
  "query": "publication-date >= 20250101 AND publication-date <= 20251231 AND buyer-country = ITA AND classification-cpv = 33122000",
  "fields": [
    "publication-number",
    "publication-date",
    "notice-title",
    "buyer-name",
    "buyer-country",
    "main-classification-proc",
    "estimated-value-proc",
    "estimated-value-cur-proc",
    "lots-max-allowed-proc"
  ],
  "page": 1,
  "limit": 1,
  "scope": "ALL",
  "checkQuerySyntax": false,
  "paginationMode": "PAGE_NUMBER",
  "onlyLatestVersions": true
}
```

`PAGE_NUMBER` mode uses `page: 1` and omits `iterationNextToken`. With nine fields and `limit: 1`, the request allows one notice and nine field values per page, within the limits of 250 notices and 10,000 field values. If there are more matches, increment `page` to retrieve them, up to the 15,000-notice limit.

### Illustrative response (`200`)

The following is a fabricated example of the expected structure, not a captured API response or a prediction of the actual matches. It assumes exactly one matching notice. Fields can be absent when the source notice does not supply them; multilingual objects use language codes such as `ita`.

```json
{
  "notices": [
    {
      "publication-number": "123456-2025",
      "publication-date": "2025-03-14",
      "notice-title": {
        "ita": "Fornitura di apparecchiature per oftalmologia"
      },
      "buyer-name": {
        "ita": [
          "Azienda sanitaria di esempio"
        ]
      },
      "buyer-country": [
        "ITA"
      ],
      "main-classification-proc": [
        "33122000"
      ],
      "estimated-value-proc": 250000.0,
      "estimated-value-cur-proc": "EUR",
      "lots-max-allowed-proc": 2
    }
  ],
  "totalNoticeCount": 1,
  "timedOut": false
}
```

No iteration token is shown because this example uses numbered pages. `lots-max-allowed-proc` is a limit on lots, not a count of all lots in the notice.

## Pagination behavior

In `PAGE_NUMBER` mode, pages can be requested independently. Results are not held in a fixed snapshot: a new OJ S release between requests can cause notices to be missed or returned twice.

In `ITERATION` mode:

1. Send the first request without `iterationNextToken`.
2. Pass the returned token as `iterationNextToken` in the next request, repeating for each batch.
3. Stop when the response contains no notices.

Iteration uses a fixed search snapshot, keeping results consistent even when notices are added or removed. The snapshot expires at the next OJ S release plus 24 hours, allowing at least 24 hours to retrieve the results.

Both modes allow at most 250 notices per request and require `fields.length × limit ≤ 10,000`.

## Errors (`400`)

| Error schema | Meaning |
|---|---|
| `QuerySyntaxErrorError` | Invalid expert-query syntax. |
| `QueryInvalidFieldFormatDetails` | A field value has an invalid format, such as an incorrectly formatted date. |
| `QueryUnknownFieldError` | The query references an unknown field. |
| `QueryUnsupportedFieldOperationError` | An operation is unsupported for the specified field. |
| `QueryUnsupportedFieldValueError` | A value is unsupported for the specified field. |
| `UnsupportedValueException` | A request parameter contains an unsupported value. |
| `ExpiredIterationTokenError` | The iteration token has expired. |
| `InvalidIterationTokenError` | The iteration token is invalid. |

Query errors can include the location of the problem (`beginLine`, `beginColumn`, `endLine`, `endColumn`) and details such as the field name, allowed format, or unsupported operation/value.