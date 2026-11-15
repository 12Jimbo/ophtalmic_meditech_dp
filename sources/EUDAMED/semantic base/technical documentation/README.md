# EUDAMED technical documentation

Reference material for understanding EUDAMED entities, fields and submission rules. Application and Public API guides are documented separately in the [user guides README](../user%20guides/README.md).

## Technical documentation

Source: [EUDAMED technical documentation](https://webgate.ec.europa.eu/eudamed-help/en/documentation/technical-documentation.html).

This material primarily serves organisations that **submit information to EUDAMED**, including through XML/data exchange, rather than consumers retrieving data through the Public API. Field definitions can help interpret API data, but submission requirements and business rules do not establish Public API filter behaviour.

| Local folder | Source section or download |
| --- | --- |
| `data dictionaries/EUD Common/` | Data dictionaries: EUD Common |
| `data dictionaries/ACT/` | Data dictionaries: Actor, ACT |
| `data dictionaries/UID Devices/` | Data dictionaries: UDI/Devices, UDI Devices; the local folder retains the spelling `UID` |
| `data dictionaries/CRF Certificates/` | Data dictionaries: Certificates, CRF certificates |
| `data dictionaries/CRF Refused Certificates and Applications/` | Data dictionaries: Certificates, CRF refused certificates and applications |
| `data dictionaries/CRF Varia/` | Data dictionaries: Certificates, CRF varia |
| `data dictionaries/CRF - CECP/` | Data dictionaries: Certificates, CRF CECP |
| `data dictionaries/MSU/` | Data dictionaries: Market Surveillance, MSU |
| `Business rules and enumerations/` | Business rules/enumerations: Common, Actor, Certificates, Market Surveillance and UDI/Devices |

The data-dictionary CSVs are local sheet exports of the source Excel workbooks. Companion `Introduction.md` files preserve introductory text and source references; they are not original Commission Markdown downloads.

### EMDN

`data dictionaries/EMDN/` has a separate source: the [European Medical Devices Nomenclature (EMDN) page](https://health.ec.europa.eu/medical-devices-topics-interest/european-medical-devices-nomenclature-emdn_en), which links to the [EMDN download browser](https://webgate.ec.europa.eu/dyna2/emdn/M90#title). The local file is `EMDN v2026_EN.csv`. It is a nomenclature catalogue, rather than an EUDAMED data-dictionary workbook.

### Business rules and enumerations

The PDFs in `Business rules and enumerations/` are downloaded from the **Business rules/enumerations** section of the technical documentation page above, preserving their original filenames. All 12 PDFs were downloaded and their PDF signatures verified on **2026-11-15**. Business rules describe validation conditions for submitted information; enumerations document permitted field values.

| Source category | Business rules PDF | Enumerations PDF |
| --- | --- | --- |
| Common | [EUD - business rules.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/EUD%20-%20business%20rules.pdf) | [EUD - enumerations.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/EUD%20-%20enumerations.pdf) |
| Actor | [AIM - business rules.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/AIM%20-%20business%20rules.pdf) | [AIM - enumerations.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/AIM%20-%20enumerations.pdf) |
| Actor | [ACT - business rules.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/ACT%20-%20business%20rules.pdf) | [ACT - enumerations.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/ACT%20-%20enumerations.pdf) |
| Certificates | [CRF - business rules.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/CRF%20-%20business%20rules.pdf) | [CRF - enumerations.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/CRF%20-%20enumerations.pdf) |
| Market Surveillance | [MSU - business rules.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/MSU%20-%20business%20rules.pdf) | [MSU - enumerations.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/MSU%20-%20enumerations.pdf) |
| UDI/Devices | [UDI Devices - business rules.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/UDI%20Devices%20-%20business%20rules.pdf) | [UDI Devices - enumerations.pdf](https://webgate.ec.europa.eu/eudamed-help/en/files/UDI%20Devices%20-%20enumerations.pdf) |
