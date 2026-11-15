# EUDAMED exploration findings

Source inventories and download provenance are maintained in the [technical documentation](semantic%20base/technical%20documentation/README.md), [user guides](semantic%20base/user%20guides/README.md) and [device registration guides](semantic%20base/device%20registration%20guides/README.md) READMEs.

## Pagination

Earlier exploration confirmed that incomplete JSON GET responses provide a continuation link for the next batch of up to 1,000 rows. This is a historical observation, not a fresh API test. See the [Public API user guide](semantic%20base/user%20guides/data%20exchange/Public%20API%20-%20user%20guide.pdf).

## Competent-authority filters

Working interpretation from the Public API guide: `CA_NAME` and `CA_ACTOR_ID` refer to competent-authority actors, corresponding to actor names and identifiers where `ACTOR_TYPE` is `Competent Authority`. Verify this mapping before using it as an authoritative filter description.

## Device identifiers

The [UDI concept infographic](semantic%20base/device%20registration%20guides/md_eudamed-udi-concept_en.pdf) explains:

- Basic UDI-DI groups devices sharing intended purpose, risk class and essential design/manufacturing characteristics.
- UDI-DI identifies a specific model, variation or version.
- Package UDI-DI identifies a container package at a packaging level.
- One Basic UDI-DI can link to multiple UDI-DIs; its registration requires at least one UDI-DI.
- Each UDI-DI inherits attributes from its Basic UDI-DI. Container-package registration is optional and can follow later.

## Nomenclature

`/udi` field `NOMENCLATURE_CODE` corresponds to the device's EMDN classification. Use the local [EMDN catalogue](semantic%20base/technical%20documentation/data%20dictionaries/EMDN/EMDN%20v2026_EN.csv) to interpret its code.
