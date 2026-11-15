# EUDAMED user guides

Source: [EUDAMED user guides and templates](https://webgate.ec.europa.eu/eudamed-help/en/documentation/user-guides-and-templates.html).

These guides describe application workflows for different users and modules, plus data exchange and Public API access. Many concern registration and submission; the Public site and Public API guides are especially relevant to retrieving information.

| Local folder | Source section |
| --- | --- |
| `actors/` | Actors: five role/site guides |
| `modules/` | Modules: four module guides |
| `data exchange/` | Data exchange: Public API guide and Swagger specification |

## PDF inventory

The current folders contain ten PDFs, with source links listed below. PDF downloads use the official `/en/files/` path; the documentation index is under `/en/documentation/`. Folder paths are relative to this README.

| Local folder | PDF download source |
| --- | --- |
| `actors/` | [Actor module for Competent Authorities - user guide.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/Actor%20module%20for%20Competent%20Authorities%20-%20user%20guide.pdf) |
| `actors/` | [Designating Authorities - user guide.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/Designating%20Authorities%20-%20user%20guide.pdf) |
| `actors/` | [Economic Operators - user guide.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/Economic%20Operators%20-%20user%20guide.pdf) |
| `actors/` | [Notified Bodies Access - user guide.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/Notified%20Bodies%20Access%20-%20user%20guide.pdf) |
| `actors/` | [Public site - user guide.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/Public%20site%20-%20user%20guide.pdf) |
| `modules/` | [Legacy Devices - user guide.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/Legacy%20Devices%20-%20user%20guide.pdf) |
| `modules/` | [UDI Devices - user guide.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/UDI%20Devices%20-%20user%20guide.pdf) |
| `modules/` | [Market Surveillance - user guide.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/Market%20Surveillance%20-%20user%20guide.pdf) |
| `modules/` | [Notified Bodies and Certificates - user guide.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/Notified%20Bodies%20and%20Certificates%20-%20user%20guide.pdf) |
| `data exchange/` | [Public API - user guide.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/Public%20API%20-%20user%20guide.pdf) |

The source page also links Technical onboarding and Third-party agreement templates in Word format; these are not part of the PDF download inventory.


## Public API specification

The local [Swagger specification](data%20exchange/swagger.yaml) accompanies the [Public API user guide](data%20exchange/Public%20API%20-%20user%20guide.pdf).

Online sources: [DG SANTE API portal](https://developer.datalake.sante.service.ec.europa.eu/api-details#api=94b9e658-d721-4b58-8d96-022c490f7a17) and the [official Swagger download](https://webgate.ec.europa.eu/eudamed-help/en/files/Swagger%20OpenAPI%20file.yaml), listed under Miscellaneous on the [technical documentation page](https://webgate.ec.europa.eu/eudamed-help/en/documentation/technical-documentation.html).

On **2026-11-15**, both the local original and [semantic_swagger.yaml](../../semantic_swagger.yaml) matched the official downloadable YAML after normalising line endings and surrounding whitespace. The published specification is version `v1.0`; its empty field descriptions and missing response schemas are also present upstream. This comparison verifies the published download, not its agreement with the running API or the portal's dynamically loaded specification.

For data dictionaries, submission rules and nomenclature provenance, see the [technical documentation README](../technical%20documentation/README.md).
