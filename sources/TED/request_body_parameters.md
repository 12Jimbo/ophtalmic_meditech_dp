# PublicExpertSearchRequestV1
**Source:** [API documentation](https://api.ted.europa.eu/swagger-ui/index.html#/Search/search)

Request body of the notice search endpoint:

| Parameter | Type | Required | Default | Constraints / Allowed Values | Description |
|---|---|---|---|---|---|
| `query` | `string` | Yes | — | Minimum 1 character | Search query used to retrieve notices. |
| `fields` | `array<string>` | Yes | — | Minimum 1 item | List of fields to include in the search results (see request_body_eample.txt). |
| `page` | `integer (int32)` | No | `1` | Minimum: `1` | Result page number, used to paginate results. |
| `limit` | `integer (int32)` | No | `10` | Minimum: `0`; maximum: 250 notices per page | Maximum number of notices returned per page. Up to 10,000 fields can be retrieved per page, calculated as `fields.length × limit`. |
| `scope` | `string` | No | `"ALL"` | `LATEST`, `ACTIVE`, `ALL` | Defines the search scope. `LATEST`: only notices from the current OJ S release. `ACTIVE`: only active notices. `ALL`: all notices. |
| `checkQuerySyntax` | `boolean` | No | `false` | `true`, `false` | When `true`, validates the query syntax without executing the search. |
| `paginationMode` | `string` | No | `"PAGE_NUMBER"` | `PAGE_NUMBER`, `ITERATION` | `PAGE_NUMBER`: standard pagination, supporting up to 15,000 notices per query. `ITERATION`: token-based pagination without a limit on total retrievable notices, but does not allow selecting a specific page. |
| `onlyLatestVersions` | `boolean` | No | `false` | `true`, `false` | When `true`, includes only the latest versions of notices. |
| `iterationNextToken` | `string` | No | — | Only applicable in `ITERATION` mode | Opaque token returned by the previous search request to retrieve the next result page. Must not be provided in `PAGE_NUMBER` mode or in the first `ITERATION` request. |

**Request URL**: https://api.ted.europa.eu/v3/notices/search

