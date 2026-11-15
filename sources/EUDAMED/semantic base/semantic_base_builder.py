"""Build the EUDAMED field map and value catalogue from the local source snapshots.

Run from any directory with Python 3.10+. CSV values remain strings, including IDs.
Mappings below are curated candidates, not automatic matches based on field names.
"""

import csv
import json
import re
from collections import Counter
from pathlib import Path


BASE = Path(__file__).resolve().parent
EUDAMED = BASE.parent
SWAGGER = BASE / "user guides/data exchange/swagger.yaml"
GUIDE = BASE / "user guides/data exchange/Public API - user guide.pdf"
DEVICE_GUIDE = BASE / "user guides/modules/UDI Devices - user guide.pdf"
LEGACY_GUIDE = BASE / "user guides/modules/Legacy Devices - user guide.pdf"
IDENTIFIERS = BASE / "device registration guides/md_eudamed-udi-concept_en.pdf"
CATEGORIES = BASE / "device registration guides/md_eudamed-devices_en.pdf"
DICTIONARIES = BASE / "technical documentation/data dictionaries"
ENUMS = BASE / "technical documentation/Business rules and enumerations"
EMDN = DICTIONARIES / "EMDN/EMDN v2026_EN.csv"
MAP_COLUMNS = [
    "endpoint", "request_field", "response_field", "request_location",
    "description", "description_source", "data_dictionary",
    "data_dictionary_field", "dictionary_enum", "mapping_status", "mapping_evidence",
]
VALUE_COLUMNS = [
    "endpoint", "field", "value", "label", "language", "value_kind",
    "value_scope", "source", "source_locator", "source_date",
]
METADATA_COLUMNS = [
    "file_name", "column_name", "data_type", "nullable", "description",
    "source", "derivation", "allowed_values", "key_role",
]


# Dictionary candidates explicitly reviewed against entity context and API samples.
ACTOR_FIELDS = {
    "ACTOR_ID": ("actor", "FLD-ACT-001"),
    "NAME": ("common", "FLD-EUD-023"),
    "ABBREVIATED_NAME": ("common", "FLD-EUD-024"),
    "STATUS_FROM_DATE": ("actor", "FLD-ACT-002"),
    "STATUS": ("actor", "FLD-ACT-003"),
    "ACTOR_TYPE": ("actor", "FLD-ACT-004"),
    "SPONSOR_TYPE": ("actor", "FLD-ACT-100"),
    "EUROPEAN_VAT_NUMBER": ("common", "FLD-EUD-032"),
    "VERSION": ("common", "FLD-EUD-013"),
    "ACT_COUNTRY_NAME": ("common", "FLD-EUD-042"),
    "ACT_COUNTRY_ISO2_CODE": ("common", "FLD-EUD-042"),
    "ACT_EMAIL": ("common", "FLD-EUD-018"),
    "ACT_TELEPHONE": ("common", "FLD-EUD-017"),
    "ACT_WEBSITE": ("common", "FLD-EUD-019"),
    "ACT_ADDR_BUILDING_NUMBER": ("common", "FLD-EUD-035"),
    "ACT_ADDR_STREET_NAME": ("common", "FLD-EUD-034"),
    "ACT_ADDR_POST_BOX": ("common", "FLD-EUD-041"),
    "ACT_ADDR_POSTAL_ZONE": ("common", "FLD-EUD-039"),
    "ACT_ADDR_CITY_NAME": ("common", "FLD-EUD-036"),
    "ACT_ADDR_COUNTRY_NAME": ("common", "FLD-EUD-042"),
    "ACT_ADDR_COUNTRY_CODE": ("common", "FLD-EUD-042"),
    "PRRC_FIRST_NAME": ("common", "FLD-EUD-048"),
    "PRRC_FAMILY_NAME": ("common", "FLD-EUD-049"),
    "CA_NAME": ("common", "FLD-EUD-023"),
    "CA_ACTOR_ID": ("actor", "FLD-ACT-001"),
}
BASIC_FIELDS = {
    "BASIC_UDI": "14", "MF_SRN": "10", "APPLICABLE_LEGISLATION_ID": "11",
    "SPECIAL_DEVICE_TYPE_ID": "13", "RISK_CLASS_ID": "16", "ANIMAL_TISSUES": "18",
    "MICROBIAL_SUBSTANCES": "34", "HUMAN_TISSUES": "23", "DEVICE_MODEL": "20",
    "DEVICE_NAME": "22", "ACTIVE": "28", "ADMINISTERING_MEDICINE": "29",
    "IMPLANTABLE": "30", "MEASURING_FUNCTION": "31", "REUSABLE": "32",
    "COMPANION_DIAGNOSTICS": "33", "NEAR_PATIENT_TESTING": "35", "SELF_TESTING": "36",
    "HUMAN_PRODUCT": "155", "MEDICINAL_PRODUCT": "158", "REAGENT": "262",
    "PROFESSIONAL_TESTING": "263", "INSTRUMENT": "264", "SUTURES": "265", "KIT": "356",
    "AR_SRN": "15",
}
UDI_FIELDS = {
    "PRIMARY_DI": "178", "TRADE_NAME": "176", "REFERENCE": "163",
    "NOMENCLATURE_CODE": "149", "LATEX": "156", "NEW_DEVICE": "159",
    "REPROCESSED": "164", "STERILE": "169", "STERILIZATION": "170",
    "DEVICE_STATUS_TYPE_ID": "130", "UNIT_OF_USE_DI": "135",
    "DIRECT_MARKETING_DI": "138", "SECONDARY_DI": "136", "CONTAINER_PACKAGE_DIS": "309",
    "SUBSTATUSES": "256", "VERSION_NUMBER": "177",
}
DEVICE_FIELDS = {key: ("basic", f"FLD-UDID-{value}") for key, value in BASIC_FIELDS.items()}
DEVICE_FIELDS.update({key: ("udi", f"FLD-UDID-{value}") for key, value in UDI_FIELDS.items()})
DEVICE_FIELDS.update({key: ("common", "FLD-EUD-023") for key in ["MF_NAME", "AR_NAME"]})
DEVICE_FIELDS.update({
    "MF_SRN": ("actor", "FLD-ACT-001"),
    "VERSION_NUMBER": ("common", "FLD-EUD-013"),
    "MEDICAL_PURPOSE": ("spp", "FLD-UDID-260"),
    "MF_ACTOR_NAMES": ("common", "FLD-EUD-023"),
    "AR_ACTOR_NAMES": ("common", "FLD-EUD-023"),
    "ACTOR_ABBREVIATED_NAMES": ("common", "FLD-EUD-024"),
})

# Start with API guide definitions, then refine reviewed subtype differences below.
GUIDE_DEFINITIONS = {
    ("/actors", "ACTOR_ID"): ("Actor identifier / Single Registration Number (SRN).", 11),
    ("/actors", "NAME"): ("Name of the actor.", 11),
    ("/actors", "ABBREVIATED_NAME"): ("Abbreviated name of the actor.", 11),
    ("/actors", "ACTOR_TYPE"): ("Role or type of the actor in EUDAMED.", 11),
    ("/actors", "ACT_COUNTRY_ISO2_CODE"): ("Two-letter country code for the country where the actor is located.", 11),
    ("/actors", "CA_NAME"): ("Name of the competent authority linked to the actor; filters actors by that authority.", 11),
    ("/actors", "CA_ACTOR_ID"): ("Actor identifier of the competent authority linked to the actor.", 11),
    ("/udi", "PRIMARY_DI"): ("Device identifier (UDI-DI) of the device.", 16),
    ("/udi", "BASIC_UDI"): ("Basic UDI-DI identifying the device family.", 16),
    ("/udi", "MF_SRN"): ("Actor identifier / SRN of the device manufacturer.", 16),
    ("/udi", "TRADE_NAME"): ("Trade name of the device.", 16),
    ("/udi", "DEVICE_NAME"): ("Name of the device.", 16),
    ("/udi", "DEVICE_MODEL"): ("Model of the device.", 16),
    ("/udi", "REFERENCE"): ("Reference or catalogue number of the device.", 16),
    ("/udi", "NOMENCLATURE_CODE"): ("EMDN classification code assigned to the device.", 16),
    ("/udi", "RISK_CLASS_ID"): ("API reference identifier for the device risk class; resolve using /reference with CODE=RISK_CLASS_ID.", 16),
    ("/udi", "APPLICABLE_LEGISLATION_ID"): ("API reference identifier for the applicable device legislation; resolve using /reference with CODE=APPLICABLE_LEGISLATION_ID.", 16),
    ("/udi", "PLACED_ON_THE_MARKET_ID"): ("API reference identifier for a market location; resolve using /reference with CODE=PLACED_ON_THE_MARKET_ID.", 16),
}
REFERENCE_FIELDS = {"RISK_CLASS_ID", "APPLICABLE_LEGISLATION_ID", "PLACED_ON_THE_MARKET_ID",
                    "SPECIAL_DEVICE_TYPE_ID", "DEVICE_STATUS_TYPE_ID", "MULTI_COMPONENT_ID", "STATUS_ID"}
TECHNICAL_ID_FIELDS = {"ID", "UUID", "UDI_DI_DATA_ULID", "BASIC_UDI_DATA_UUID", "BASIC_UDI_DATA_ULID"}

# Reviewed export descriptions distinguish business identifiers from technical IDs.
REVIEWED_DESCRIPTIONS = {
    ("/actors", "VERSION"): "Version number of the exported actor information.",
    ("/actors", "STATUS_FROM_DATE"): "Date from which the actor's current activity status applies.",
    ("/actors", "ACT_COUNTRY_NAME"): "Name of the country associated with the actor.",
    ("/actors", "ACT_ADDR_COUNTRY_NAME"): "Name of the country in the actor's address.",
    ("/actors", "ACT_ADDR_COUNTRY_CODE"): "Country code in the actor's address, using the API's country representation.",
    ("/actors", "ACT_COUNTRY_TYPE"): "Country category associated with the actor; API codes distinguish EU member states, extended/special groups and non-EU countries.",
    ("/actors", "ACT_ADDR_COUNTRY_TYPE"): "Country category associated with the actor address; API code spellings must not be equated automatically with dictionary labels.",
    ("/actors", "PRRC_FIRST_NAME"): "Given name of a person responsible for regulatory compliance associated with the actor.",
    ("/actors", "PRRC_FAMILY_NAME"): "Family name of a person responsible for regulatory compliance associated with the actor.",
    ("/udi", "PRIMARY_DI"): "Device-level regulatory identifier: UDI-DI for regulation devices and SPPs; a legacy device can instead carry a generated EUDAMED ID. This is not the exported UUID or numeric ID.",
    ("/udi", "BASIC_UDI"): "Group/model-level regulatory identifier: Basic UDI-DI for regulation devices and SPPs; EUDAMED DI for legacy devices. Distinct from BASIC_UDI_DATA_UUID and BASIC_UDI_DATA_ULID.",
    ("/udi", "MF_SRN"): "Actor identifier/SRN of the manufacturer, or of the system/procedure-pack producer for SPP records.",
    ("/udi", "MF_NAME"): "Scalar exported name of the manufacturer or SPP producer; the language-selection rule is not documented.",
    ("/udi", "MF_ACTOR_NAMES"): "Language-tagged organisation names of the manufacturer or SPP producer; the CSV cell contains JSON text with a texts array. The native API JSON type is not established by this CSV.",
    ("/udi", "AR_NAME"): "Scalar exported name of the authorised representative; the language-selection rule is not documented.",
    ("/udi", "AR_ACTOR_NAMES"): "Language-tagged organisation names of the authorised representative; the CSV cell contains JSON text with a texts array. The native API JSON type is not established by this CSV.",
    ("/udi", "ACTOR_ABBREVIATED_NAMES"): "Language-tagged abbreviated organisation names stored as JSON text in the CSV; manufacturer/SPP-producer association is supported by overlapping sampled actors but is not an explicit API crosswalk.",
    ("/udi", "MEDICAL_PURPOSE"): "Medical purpose of the system or procedure pack, exported as text; the dictionary defines multilingual content, but the scalar selection rule is undocumented.",
    ("/udi", "DEVICE_CRITERION"): "Export classification distinguishing STANDARD, LEGACY and SPP records. The association with regulation devices, legacy devices and system/procedure packs is inferred from registration documentation and sample patterns.",
    ("/udi", "MULTI_COMPONENT_ID"): "API reference identifier distinguishing systems/procedure packs that are devices in themselves from SPP systems/procedure packs. The export appears to combine subtype-specific dictionary concepts.",
    ("/udi", "SPECIAL_DEVICE_TYPE_ID"): "API reference identifier for the special device type; the candidate dictionary describes the underlying type rather than its API ID.",
    ("/udi", "STATUS_ID"): "API activity-status reference identifier with active/inactive labels in the reference sample. Its precise entity/lifecycle scope is undocumented; it is not established as a workflow state or market-status field.",
    ("/udi", "CMR_SUBSTANCE"): "Candidate presence indicator for carcinogenic, mutagenic or toxic-for-reproduction substances; sampled exports use 0/1 or missing values. The transformation from substance details to this indicator is undocumented.",
    ("/udi", "ENDOCRINE_DISRUPTOR"): "Candidate presence indicator for endocrine-disrupting substances. Only 0 and missing values occur in this sample; absence of observed 1 does not establish a restricted value domain.",
    ("/udi", "ID"): "Numeric technical identifier exported by /udi. Entity/version scope and persistence are undocumented; do not treat it as a UDI-DI or EUDAMED ID.",
    ("/udi", "UUID"): "UUID-format technical identifier exported with a device row. Entity/version scope and persistence are undocumented; distinct from the regulatory identifiers PRIMARY_DI and BASIC_UDI.",
    ("/udi", "UDI_DI_DATA_ULID"): "ULID-format technical identifier exported with device-level data. The name suggests UDI-DI data, but its entity/version scope and persistence are not established.",
    ("/udi", "BASIC_UDI_DATA_UUID"): "UUID-format technical identifier associated with the group/basic-level data in the sample. Its persistence and exact entity/version scope are undocumented; it is not BASIC_UDI.",
    ("/udi", "BASIC_UDI_DATA_ULID"): "ULID-format technical identifier associated with the group/basic-level data in the sample. Its persistence and exact entity/version scope are undocumented; it is not BASIC_UDI.",
    ("/udi", "LATEST_VERSION"): "Exported latest-version marker. The sample contains only 1; whether latest means registered, published or otherwise available version is not established.",
    ("/udi", "VERSION_NUMBER"): "Version number of the exported device information; distinct from the latest-version marker and the technical identifiers.",
    ("/udi", "NOMENCLATURE_CODE"): "EMDN classification code(s) assigned to the device. Multiple codes can be exported in one comma-separated cell; request matching semantics are not established by that representation.",
    ("/udi", "CONTAINER_PACKAGE_DIS"): "Container-package UDI-DI values associated with the device, exported as a comma-separated list when multiple are present. Container packages are packaging levels, not systems/procedure packs.",
    ("/udi", "DIRECT_MARKETING_DI"): "Candidate direct-marking UDI-DI; the API export spells the field DIRECT_MARKETING_DI. It can equal the primary DI or a different DI; the spelling equivalence remains inferred.",
    ("/udi", "ACTIVE"): "Whether the device is an active device in the registration sense (operation depends on an energy source); not the record's active/inactive status.",
    ("/udi", "REUSABLE"): "Whether the device is a reusable surgical instrument; not a generic statement that any device can be reused.",
    ("/udi", "STERILIZATION"): "Whether sterilisation is needed before use; not a record that sterilisation has already been performed.",
    ("/udi", "NEW_DEVICE"): "IVDR new-device indicator under the dictionary's three-year availability/analytical-technology criteria; not a general flag that an exported record was recently created.",
    ("/udi", "COMPANION_DIAGNOSTICS"): "Whether the device is essential to the safe and effective use of a corresponding medicinal product, identifying patients likely to benefit or at increased risk of serious adverse reactions.",
    ("/udi", "IMPLANTABLE"): "Whether the device is implantable; the dictionary includes partially introduced devices intended to remain after clinical intervention for at least 30 days, and specifies false by default for Class I devices.",
    ("/udi", "NEAR_PATIENT_TESTING"): "Whether the device is intended for testing outside a laboratory, generally near the patient by a health professional, rather than self-testing.",
    ("/udi", "SELF_TESTING"): "Whether the manufacturer intends the device for use by lay persons, including devices used for testing services offered through information society services.",
    ("/udi", "SUTURES"): "Indicator for the dictionary's listed implantable-device exceptions: sutures, staples, dental fillings/braces, tooth crowns, screws, wedges, plates/wires, pins, clips and connectors. The dictionary limits applicability to implantable Class IIb devices; the field covers more than sutures.",
    ("/udi", "SUBSTATUSES"): "Exported device-substatus information. The sample contains only missing values, so its populated representation and cardinality are not established.",
}


def relative(path):
    """Store portable paths relative to the EUDAMED folder."""
    return path.relative_to(EUDAMED).as_posix()


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields, rows = list(reader.fieldnames or []), list(reader)
    require(fields and len(fields) == len(set(fields)), f"Missing or repeated CSV headers: {path}")
    require(all(None not in row and all(value is not None for value in row.values()) for row in rows),
            f"CSV record width does not match headers: {path}")
    return fields, rows


def require(condition, message):
    if not condition:
        raise ValueError(message)


def request_parameters():
    """Read the parameter subset of the checked-in, consistently indented Swagger."""
    text = SWAGGER.read_text(encoding="utf-8-sig")
    sections = list(re.finditer(r"^  (/[^:]+):\s*$", text, re.MULTILINE))
    parameters = {}
    for index, section in enumerate(sections):
        end = sections[index + 1].start() if index + 1 < len(sections) else text.index("\ncomponents:")
        block = text[section.end():end].split("      responses:")[0]
        entries = list(re.finditer(r"^        - name: (.+)$", block, re.MULTILINE))
        endpoint_parameters = {}
        for position, entry in enumerate(entries):
            end = entries[position + 1].start() if position + 1 < len(entries) else len(block)
            definition = block[entry.end():end]
            location = re.search(r"^          in: (.+)$", definition, re.MULTILINE).group(1)
            enums = re.findall(r"^              - (.+)$", definition, re.MULTILINE)
            if entry.group(1) in endpoint_parameters:
                raise ValueError("Repeated parameter name requires review of request_location and row identity")
            endpoint_parameters[entry.group(1)] = {"location": location, "enum": enums}
        parameters[section.group(1)] = endpoint_parameters
    require(set(parameters) == {"/actors", "/reference", "/udi"}, "Unexpected Swagger endpoint inventory")
    return parameters


def dictionary_rows():
    paths = {
        "actor": DICTIONARIES / "ACT/ACT - data dictionary-Actor.csv",
        "common": DICTIONARIES / "EUD Common/EUD - data dictionary-Common Entities.csv",
        "basic": DICTIONARIES / "UID Devices/UDI Devices - data dictionary-DD BASIC UDI.csv",
        "udi": DICTIONARIES / "UID Devices/UDI Devices - data dictionary-DD UDI-DI.csv",
        "spp": DICTIONARIES / "UID Devices/UDI Devices - data dictionary-DD BASIC UDI_SPP.csv",
        "legacy": DICTIONARIES / "UID Devices/UDI Devices - data dictionary-DD Legacy Devices.csv",
    }
    lookup = {}
    for group, path in paths.items():
        with path.open(encoding="utf-8-sig", newline="") as handle:
            records = list(csv.reader(handle))
        header = next(i for i, row in enumerate(records) if "Field ID" in [cell.strip() for cell in row])
        columns = [cell.strip() for cell in records[header]]
        for record in records[header + 1:]:
            row = dict(zip(columns, record))
            field = row.get("Field ID", "").strip()
            if field:
                lookup.setdefault((group, field), (path, row))
    return lookup


def clean(text):
    return " ".join(text.split())


def present(value):
    """Treat only empty cells and the sample's literal NULL marker as missing."""
    return value not in {"", "NULL"}


def text_items(value):
    """Inspect multilingual exports without replacing their original CSV text."""
    try:
        payload = json.loads(value)
        return [item["text"] for item in payload["texts"]]
    except (ValueError, KeyError, TypeError):
        return None


def sample_evidence(endpoint, field, samples):
    """Compute evidence from current snapshots, rather than hard-code sample counts."""
    _, fields, records = samples[endpoint]
    if field not in fields:
        return "", False
    values = [row[field] for row in records if present(row[field])]
    counts = Counter(values)
    notes = [f"Sample: {len(values)}/{len(records)} nonmissing, {len(counts)} distinct nonmissing values; empty/NULL is not interpreted as false."]
    conflict = False
    if field in {"MF_ACTOR_NAMES", "AR_ACTOR_NAMES", "ACTOR_ABBREVIATED_NAMES"}:
        counterpart = {"MF_ACTOR_NAMES": "MF_NAME", "AR_ACTOR_NAMES": "AR_NAME"}.get(field)
        parsed = [text_items(value) for value in values]
        valid = sum(items is not None for items in parsed)
        notes.append(f"{valid}/{len(values)} populated cells parse as JSON with a texts array.")
        conflict = valid != len(values)
        if counterpart:
            compared = [row for row in records if present(row[field]) and present(row[counterpart])]
            matched = sum(row[counterpart] in (text_items(row[field]) or []) for row in compared)
            notes.append(f"Scalar {counterpart} is a member of that texts array in {matched}/{len(compared)} comparable rows; language preference is not established.")
            conflict |= matched != len(compared)
        else:
            actors = {row["ACTOR_ID"]: row for row in samples["/actors"][2]}
            compared = [row for row in records if row["MF_SRN"] in actors and present(row[field])
                        and present(actors[row["MF_SRN"]]["ABBREVIATED_NAME"])]
            matched = sum(actors[row["MF_SRN"]]["ABBREVIATED_NAME"] in (text_items(row[field]) or []) for row in compared)
            notes.append(f"Joining MF_SRN to sampled ACTOR_ID gives {matched}/{len(compared)} comparable abbreviation memberships; limited overlap is supporting evidence, not a complete crosswalk.")
            conflict |= matched != len(compared)
    if endpoint == "/udi" and field in {"MEDICAL_PURPOSE", "MF_SRN", "PRIMARY_DI", "BASIC_UDI", "MULTI_COMPONENT_ID"}:
        for criterion in sorted({row["DEVICE_CRITERION"] for row in records}):
            subset = [row for row in records if row["DEVICE_CRITERION"] == criterion]
            populated = [row[field] for row in subset if present(row[field])]
            detail = f"{criterion}: {len(populated)}/{len(subset)} populated"
            if field == "MF_SRN":
                roles = Counter(value.split("-")[1] if "-" in value else "unknown" for value in populated)
                detail += f", SRN role segments {dict(sorted(roles.items()))}"
            elif field in {"PRIMARY_DI", "BASIC_UDI"}:
                detail += f", B- prefix {sum(v.startswith('B-') for v in populated)}, D- prefix {sum(v.startswith('D-') for v in populated)}"
            elif field == "MULTI_COMPONENT_ID":
                detail += f", reference IDs {sorted(set(populated))}"
            notes.append(detail + ".")
    if field in {"CMR_SUBSTANCE", "ENDOCRINE_DISRUPTOR", "LATEST_VERSION", "DEVICE_CRITERION",
                 "ACT_COUNTRY_TYPE", "ACT_ADDR_COUNTRY_TYPE"}:
        notes.append(f"Observed nonmissing distribution: {dict(sorted(counts.items()))}; not an exhaustive allowed-value domain.")
    if field in {"NOMENCLATURE_CODE", "CONTAINER_PACKAGE_DIS"}:
        notes.append(f"{sum(',' in value for value in values)} populated cells contain comma-separated values; field_values retains these complete cells as observations.")
    if field in TECHNICAL_ID_FIELDS and endpoint == "/udi":
        pattern = (r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}" if "UUID" in field
                   else r"[0-7][0-9A-HJKMNP-TV-Z]{25}" if "ULID" in field else r"[0-9]+")
        notes.append(f"{sum(bool(re.fullmatch(pattern, value)) for value in values)}/{len(values)} populated values match the stated identifier format; format does not establish entity scope, a global key or persistence.")
        notes.append(f"No regulatory-identifier equivalence is asserted; sampled equality counts are PRIMARY_DI={sum(row[field] == row['PRIMARY_DI'] for row in records)}, BASIC_UDI={sum(row[field] == row['BASIC_UDI'] for row in records)}.")
        if field.startswith("BASIC_UDI_DATA_"):
            groups = {}
            for row in records:
                groups.setdefault(row[field], set()).add(row["BASIC_UDI"])
            notes.append(f"The largest sampled mapping from this technical value to BASIC_UDI has {max(map(len, groups.values()), default=0)} distinct values; this is an observation, not a foreign-key guarantee.")
    return " ".join(notes), conflict


def review_mapping(row, field, samples, lookup):
    """Apply reviewed definitions and retain subtype-specific or unresolved scope."""
    endpoint = row["endpoint"]
    notes = []
    if (endpoint, field) in REVIEWED_DESCRIPTIONS:
        row["description"] = REVIEWED_DESCRIPTIONS[endpoint, field]
        if not row["description_source"]:
            row["description_source"] = f"{relative(samples[endpoint][0])}#column={field}"
    if endpoint == "/udi" and field in {"PRIMARY_DI", "BASIC_UDI"}:
        legacy_id = "FLD-UDID-342" if field == "PRIMARY_DI" else "FLD-UDID-42"
        legacy_path, _ = lookup["legacy", legacy_id]
        notes.append(f"Legacy variant: {relative(legacy_path)}#{legacy_id}; {relative(LEGACY_GUIDE)}#pdf-page=4 explains EUDAMED DI/ID and UDI-DI alternatives. The recorded standard-device dictionary candidate does not cover every subtype by itself.")
        notes.append(f"{relative(IDENTIFIERS)}#pdf-page=1 defines Basic UDI-DI, UDI-DI and package UDI-DI; it does not define API numeric ID, UUID or ULID fields.")
        row["description_source"] = f"{relative(LEGACY_GUIDE)}#pdf-page=4" if field == "PRIMARY_DI" else f"{relative(IDENTIFIERS)}#pdf-page=1"
    if endpoint == "/udi" and field in TECHNICAL_ID_FIELDS:
        notes.append(f"Reviewed {relative(IDENTIFIERS)}#pdf-page=1 and {relative(CATEGORIES)}#pdf-page=1: these define regulatory identifiers/device categories, not the scope of this technical export field.")
    if endpoint == "/actors" and field in {"CA_NAME", "CA_ACTOR_ID"}:
        path, _ = lookup["actor", "FLD-ACT-012"]
        notes.append(f"Projected through responsible competent authority {relative(path)}#FLD-ACT-012 (an Actor relation). The candidate identifies the related actor's scalar name/identifier, not the parent relation itself; no explicit API crosswalk is supplied.")
    if endpoint == "/udi" and field in {"MF_SRN", "MF_NAME", "MF_ACTOR_NAMES", "ACTOR_ABBREVIATED_NAMES"}:
        path, _ = lookup["spp", "FLD-UDID-44"]
        notes.append(f"Actor role is subtype-dependent: manufacturer FLD-UDID-10 for regulation/legacy devices; SPP producer {relative(path)}#FLD-UDID-44 for SPPs. Do not restrict MF-prefixed exports to manufacturer actors.")
    if (endpoint, field) in {("/udi", "VERSION_NUMBER"), ("/actors", "VERSION")}:
        notes.append("The scalar candidate is VersionData.FLD-EUD-013 (Version Number), not the parent VersionData relation FLD-UDID-177 or FLD-ACT-015.")
        row["description_source"] = f"{row['data_dictionary']}#{row['data_dictionary_field']}"
    if endpoint == "/udi" and field in {"CMR_SUBSTANCE", "ENDOCRINE_DISRUPTOR"}:
        related = "FLD-UDID-140" if field == "CMR_SUBSTANCE" else "FLD-UDID-310"
        notes.append(f"{relative(DEVICE_GUIDE)}#pdf-page=25 discusses substance presence/details. Dictionary {related} describes a substance list, so it is related evidence, not a direct scalar-flag mapping. Missing values are not false.")
        row.update(description_source=f"{relative(DEVICE_GUIDE)}#pdf-page=25", mapping_status="inferred")
    if field in {"ACT_COUNTRY_TYPE", "ACT_ADDR_COUNTRY_TYPE"}:
        notes.append(f"{relative(ENUMS / 'EUD - enumerations.pdf')}#pdf-pages=3-4 contains country-group labels. The sample uses different tokens, so no exact dictionary-code conversion or single field mapping is asserted.")
        row["mapping_status"] = "inferred"
    if endpoint == "/udi" and field in {"DEVICE_CRITERION", "MULTI_COMPONENT_ID"}:
        row["mapping_status"] = "inferred"
        if field == "DEVICE_CRITERION":
            row["description_source"] = f"{relative(CATEGORIES)}#pdf-page=1"
            notes.append("The infographic supplies device-category concepts, not the literal API enum STANDARD/LEGACY/SPP. The literal tokens and their associations are observed in the sample.")
        else:
            row["description_source"] = f"{relative(samples['/reference'][0])}#CODE=MULTI_COMPONENT_ID"
            notes.append(f"The export appears to combine the ordinary-device System/Procedure Pack concept FLD-UDID-12 with SPP type {relative(lookup['spp', 'FLD-UDID-261'][0])}#FLD-UDID-261; no single universal dictionary field is assigned.")
    if endpoint == "/udi" and field == "STATUS_ID":
        row["description_source"] = f"{relative(samples['/reference'][0])}#CODE=STATUS_ID"
        notes.append("Reference labels include Aktiv and Inactief/Inaktiv for the observed IDs; do not substitute market availability (DEVICE_STATUS_TYPE_ID), active-device design (ACTIVE), or VersionData workflow state (FLD-EUD-014). Exact lifecycle scope remains unresolved.")
    if field == "MEDICAL_PURPOSE":
        notes.append("SPP-only applicability is supported by the current sample, not enforced as an API-wide nullability rule.")
    if endpoint == "/udi" and field == "PLACED_ON_THE_MARKET_ID":
        row["mapping_status"] = "inferred"
        notes.append("Country/market-location meaning is supported by reference labels; the malformed guide description is not a complete definition.")
    profile, conflict = sample_evidence(endpoint, field, samples)
    if profile:
        notes.append(profile)
    if conflict:
        row["mapping_status"] = "unresolved"
        notes.append("Current sample contradicts part of the curated name-projection interpretation; review required.")
    return notes


def build_semantic_base(parameters, samples):
    lookup = dictionary_rows()
    result = []
    for endpoint, request in parameters.items():
        sample_path, response_fields, _ = samples[endpoint]
        # Pair only identical names within the same endpoint, keeping request-only filters.
        fields = list(request) + [field for field in response_fields if field not in request]
        for field in fields:
            row = dict.fromkeys(MAP_COLUMNS, "")
            row.update(endpoint=endpoint, request_field=field if field in request else "",
                       response_field=field if field in response_fields else "",
                       request_location=request[field]["location"] if field in request else "",
                       mapping_status="unresolved")
            evidence = []
            if row["request_field"]:
                evidence.append(f"{relative(SWAGGER)}: GET {endpoint} parameter {field}.")
            if row["response_field"]:
                evidence.append(f"{relative(sample_path)}: header {field}.")
            if row["request_field"] and row["response_field"]:
                evidence.append("Request/response pairing uses the same endpoint and exact field name; matching behaviour is not established by the sample.")
            candidate = (ACTOR_FIELDS if endpoint == "/actors" else DEVICE_FIELDS if endpoint == "/udi" else {}).get(field)
            if candidate:
                path, definition = lookup[candidate]
                row.update(data_dictionary=relative(path), data_dictionary_field=candidate[1],
                           dictionary_enum=clean(definition.get("ENUM Reference Code", "")),
                           description=clean(definition.get("Field Description / Notes", "")),
                           description_source=f"{relative(path)}#{candidate[1]}", mapping_status="inferred")
                evidence.append(f"Candidate {candidate[1]} ({clean(definition.get('Field Label', ''))}) agrees with entity context; no explicit API-to-dictionary crosswalk was found.")
            if (endpoint, field) in GUIDE_DEFINITIONS:
                row["description"], page = GUIDE_DEFINITIONS[endpoint, field]
                row["description_source"] = f"{relative(GUIDE)}#pdf-page={page}"
                evidence.append(f"API guide PDF page {page} documents the API concept; dictionary identity remains inferred where a candidate is recorded.")
                if not candidate:
                    row["mapping_status"] = "verified"
            if field in {"format", "Content-Type"}:
                row.update(description="Response serialization format." if field == "format" else "Request media type; the Swagger specifies application/json as the default.",
                           description_source=f"{relative(SWAGGER)}#GET {endpoint} {field}", mapping_status="verified")
            if endpoint == "/reference" and field in response_fields:
                row.update(description={"ID": "Identifier of a reference value within a reference category; use with CODE and LANGUAGE to resolve a label.",
                                        "CODE": "Reference category naming the field whose IDs are being resolved, for example RISK_CLASS_ID.",
                                        "LANGUAGE": "Language code of the reference-value label.",
                                        "VALUE": "Localized label for the reference identifier and category."}[field],
                           description_source=f"{relative(GUIDE)}#pdf-pages=4,15-16", mapping_status="verified")
            if field.startswith("PRRC_"):
                evidence.append("Projected person-name component is inferred through Actor.PRRC (FLD-ACT-006), not an explicit API crosswalk.")
            if endpoint == "/actors" and field == "STATUS":
                evidence.append("Dictionary names ENUM_ACT_ACTIVITY_STATUS; the ACT enumeration PDF calls its active/inactive list actor-statusEnum / ENUM_ACT_STATUS. Equivalence is not explicitly established.")
            if field == "PRIMARY_DI":
                evidence.append("Guide page 13 uses PRIMARY_UDI, but page 16 and Swagger use PRIMARY_DI. Legacy alternatives are qualified by the registration guide and dictionary evidence below.")
            if field == "PLACED_ON_THE_MARKET_ID":
                evidence.append("Guide page 16 misspells the parameter placecd_on_the_market_id. Reference sample includes non-EU countries, so no EU-only dictionary field is assigned.")
            if field == "DIRECT_MARKETING_DI":
                evidence.append("Possible API spelling anomaly: candidate dictionary says Direct Marking; mapping is not verified.")
            if field in {"RISK_CLASS_ID", "APPLICABLE_LEGISLATION_ID"}:
                evidence.append("Guide calls the parameter a string; Swagger calls it a number. Dictionary enum codes are not API numeric IDs.")
            evidence.extend(review_mapping(row, field, samples, lookup))
            if not row["description"]:
                evidence.append("No defensible business definition assigned; field is retained for review.")
            row["mapping_evidence"] = " ".join(evidence)
            result.append(row)
    return result


def build_field_values(parameters, samples):
    rows = []

    def add(endpoint, field, value, label, kind, scope, path, locator, language=""):
        rows.append(dict(zip(VALUE_COLUMNS, [endpoint, field, value, label, language, kind,
                                            scope, relative(path), locator, ""])))

    # Sample values are observations, including atomic exports of list-like fields.
    for endpoint, (path, fields, records) in samples.items():
        for field in fields:
            values = sorted({record[field] for record in records if present(record[field])})
            for value in values:
                add(endpoint, field, value, "", "observed", "response", path, f"column={field}")
        for field, parameter in parameters[endpoint].items():
            for value in parameter["enum"]:
                add(endpoint, field, value, "", "allowed", "request", SWAGGER, f"GET {endpoint} parameter {field}: enum")

    # Keep every language and category-qualified ID; do not join reference rows on ID alone.
    reference_path, _, reference = samples["/reference"]
    for record in reference:
        if record["CODE"] in REFERENCE_FIELDS and record["ID"] not in {"", "NULL"}:
            add("/udi", record["CODE"], record["ID"], record["VALUE"], "reference-listed",
                "request_response" if record["CODE"] in parameters["/udi"] else "response",
                reference_path, f"CODE={record['CODE']};ID={record['ID']};LANGUAGE={record['LANGUAGE']}", record["LANGUAGE"])

    # EMDN is a versioned classification catalogue, not proof of observed API acceptance.
    _, records = read_csv(EMDN)
    for record in records:
        add("/udi", "NOMENCLATURE_CODE", record["CODE"], record["TERM EMDN (v.2026)"],
            "reference-listed", "dictionary", EMDN, f"CODE={record['CODE']};version=2026", "en")

    # Curated legible lists from official PDFs; submission codes stay dictionary-scoped.
    for label in ["Competent Authority", "Designating Authority", "Importer", "Authorised Representative",
                  "System/Procedure Pack Producer", "Manufacturer", "Notified Body"]:
        add("/actors", "ACTOR_TYPE", label, label, "allowed", "request", GUIDE, "pdf-page=11;actor_type", "en")
    actor_enums = {
        "ACTOR_TYPE": ("pdf-pages=3-4;actor-typeEnum", [
            "authorised-representative", "competent-authority", "designating-authority",
            "european-commission", "importer", "manufacturer", "notified-body", "sponsor",
            "system-procedure-pack-producer"]),
        "STATUS": ("pdf-page=4;actor-statusEnum", ["active", "inactive"]),
        "SPONSOR_TYPE": ("pdf-page=4;sponsor-typeEnum", ["individual", "company", "institution", "organisation"]),
    }
    for field, (locator, entries) in actor_enums.items():
        for value in entries:
            add("/actors", field, value, "", "allowed", "dictionary", ENUMS / "ACT - enumerations.pdf", locator)
    enum_lists = [
        ("MULTI_COMPONENT_ID", "UDI Devices - enumerations.pdf", "pdf-pages=16-17;ENUM_UDID_MultiComponentType",
         [("SYSTEM", "System which is a device in itself"), ("PROCEDURE_PACK", "Procedure Pack which is a device in itself"),
          ("SPP_SYSTEM", "SPP System"), ("SPP_PROCEDURE_PACK", "SPP Procedure Pack")]),
        ("SUBSTATUSES", "UDI Devices - enumerations.pdf", "pdf-page=18;DeviceSubstatusEnum",
         [("RECALLED", "Recalled"), ("FIELD_SAFETY_CORRECTIVE_ACTION_INITIATED", "Field safety corrective action initiated")]),
    ]
    for field, filename, locator, entries in enum_lists:
        for value, label in entries:
            add("/udi", field, value, label, "allowed", "dictionary", ENUMS / filename, locator, "en")
    # Preserve first occurrence while eliminating repeated source records.
    unique = {tuple(row[column] for column in VALUE_COLUMNS): row for row in rows}
    return sorted(unique.values(), key=lambda row: tuple(row[column] for column in VALUE_COLUMNS))


def metadata_row(file_name, column, description, source, derivation="", nullable="yes", allowed="", key=""):
    return dict(zip(METADATA_COLUMNS, [file_name, column, "string", nullable, description, source,
                                       derivation, allowed, key]))


def build_metadata():
    swagger_source = relative(SWAGGER)
    sample_sources = "; ".join(f"data samples/eudamed api {name}.csv#header" for name in ["actors", "reference", "udi"])
    definitions = {
        "endpoint": ("API endpoint path.", f"{swagger_source}#/paths", "Part of field identity; endpoint plus coalesce(response_field, request_field) is unique in this output.", "no", "/actors;/reference;/udi"),
        "request_field": ("Exact Swagger request parameter name, including headers.", f"{swagger_source}#/paths/*/get/parameters/name", "Blank when no such parameter is declared in Swagger. Same-name pairing with a sampled response field is endpoint-local, not a proof of filter behaviour.", "yes", ""),
        "response_field": ("Exact response-column name observed in the local samples.", sample_sources, "Blank when absent from sample headers; does not prove the API can never return it. At least one of request_field or response_field must be populated.", "yes", ""),
        "request_location": ("Swagger parameter location.", f"{swagger_source}#/paths/*/get/parameters/in", "Blank exactly when request_field is blank; current catalogue has query/header parameters only.", "yes", "query;header"),
        "description": ("Business meaning or explicitly qualified structural/candidate interpretation.", "See description_source and mapping_evidence in semantic_base.csv", "Review combines guides, dictionary definitions and computed sample evidence. Subtype and representation differences are retained. A populated description does not imply a resolved mapping.", "yes", ""),
        "description_source": ("Principal definition source, relative to sources/EUDAMED, with a locator after #.", "Reviewed local source identified for each semantic_base.csv row", "Additional supporting/conditional sources are recorded in mapping_evidence. pdf-page uses physical pages including cover pages; a dictionary locator is its Field ID.", "yes", ""),
        "data_dictionary": ("EUDAMED-relative CSV path for one reviewed dictionary candidate.", "See dictionary_rows() and curated candidates in semantic base/semantic_base_builder.py", "A representative candidate is not universal equivalence: subtype alternatives and parent-to-scalar projections are explained in mapping_evidence. Blank can mean a composite export or no defensible single field.", "yes", ""),
        "data_dictionary_field": ("Field ID of the candidate in data_dictionary.", "Field ID column of the CSV named in data_dictionary", "Path plus Field ID identifies the source record; IDs may recur across sheets. Both dictionary columns are blank or populated together. This is not an API field ID.", "yes", ""),
        "dictionary_enum": ("Raw enum reference attached to the selected candidate dictionary record.", "ENUM Reference Code column of the CSV named in data_dictionary", "Whitespace collapsed only; may contain multiple references/prose. Neither a complete value list nor a translation to API numeric IDs.", "yes", ""),
        "mapping_status": ("Conservative review status covering the recorded interpretation and links.", "Curated review plus current source/sample checks in semantic base/semantic_base_builder.py", "verified: direct documented API definition with no unverified dictionary link; inferred: supported business meaning or candidate projection/link; unresolved: identity/scope or conflicting evidence remains material. No dictionary crosswalk is currently explicitly verified.", "no", "verified;inferred;unresolved"),
        "mapping_evidence": ("Source locators, conditional variants, sample counts and remaining uncertainty.", "Swagger, dictionaries, cited PDFs and current response samples", "Computed counts describe this snapshot only. Exact-name pairing, format checks and sampled uniqueness do not establish filter semantics, global keys, persistence or universal cardinality.", "no", ""),
    }
    rows = [metadata_row("semantic_base.csv", column, *definitions[column]) for column in MAP_COLUMNS]
    values = {
        "endpoint": ("Endpoint whose field has this value.", "semantic base/semantic_base.csv#endpoint", "Join to endpoint plus field; value rows are evidence, not a complete allowed-value dimension.", "no", "/actors;/reference;/udi"),
        "field": ("Canonical API field name: response_field when present, otherwise request_field.", "semantic base/semantic_base.csv#request_field,response_field", "Join using endpoint and coalesce(response_field, request_field); not unique alone.", "no", ""),
        "value": ("Exact observed value, reference ID, enumeration code or documented request option.", "Source named by source and source_locator", "All values remain strings; NULL sample markers and empty cells are excluded; list-like export strings are not split.", "no", ""),
        "label": ("Source-provided display label where available.", f"data samples/eudamed api reference.csv#VALUE; {relative(EMDN)}#TERM EMDN (v.2026); source/source_locator for PDF entries", "Blank where a source provides no label; dictionary code labels are kept separate from API numeric-ID labels. No numeric-ID translations are invented.", "yes", ""),
        "language": ("Source language of the label, preserved where supplied.", "data samples/eudamed api reference.csv#LANGUAGE; English version of EMDN and cited PDF pages", "Blank if no label language is specified; reference languages are preserved without substituting English for missing translations.", "yes", ""),
        "value_kind": ("Evidence class for this value.", "Source type and reviewed lists in semantic base/semantic_base_builder.py", "allowed means explicitly listed at value_scope, not necessarily exhaustive; reference-listed is a catalogue entry, not an acceptance test; observed means a whole nonmissing sample cell.", "no", "allowed;reference-listed;observed"),
        "value_scope": ("Representation to which the source value applies.", "Reviewed source context", "dictionary values are candidate submission representations, not verified API IDs/inputs; request_response qualifies an API reference ID for a request field also observed in the response. Always retain main-row mapping qualifications.", "no", "request;response;request_response;dictionary"),
        "source": ("EUDAMED-relative source file path.", "Local source snapshot", "Source provenance, not a claim of completeness or freshness.", "no", ""),
        "source_locator": ("Column, reference key, PDF page/enum or EMDN version locating the evidence.", "Source-specific identifiers", "Reference IDs are qualified by CODE and LANGUAGE.", "no", ""),
        "source_date": ("Known source extraction/publication date in YYYY-MM-DD format.", "Explicit full source date only", "Blank in current undated snapshots; year/version or filesystem/build timestamps are not substituted. Logical date type, serialized as ISO text when known.", "yes", "YYYY-MM-DD when populated"),
    }
    rows.extend(metadata_row("field_values.csv", column, *values[column]) for column in VALUE_COLUMNS)
    for row in rows:
        if row["file_name"] == "field_values.csv" and row["column_name"] == "source_date":
            row["data_type"] = "date"
        if row["column_name"] == "endpoint":
            row["key_role"] = "field identity component; not unique alone"
        elif row["file_name"] == "semantic_base.csv" and row["column_name"] in {"request_field", "response_field"}:
            row["key_role"] = "field identity: endpoint plus coalesce(response_field, request_field)"
        elif row["file_name"] == "field_values.csv" and row["column_name"] == "field":
            row["key_role"] = "field identity component; foreign key with endpoint"
    return rows


def build_tables():
    parameters = request_parameters()
    samples = {}
    for endpoint in parameters:
        path = EUDAMED / "data samples" / f"eudamed api {endpoint[1:]}.csv"
        fields, records = read_csv(path)
        samples[endpoint] = path, fields, records
    semantic = build_semantic_base(parameters, samples)
    values = build_field_values(parameters, samples)
    validate(semantic, values, parameters, samples)
    metadata = build_metadata()
    for filename, columns in [("semantic_base.csv", MAP_COLUMNS), ("field_values.csv", VALUE_COLUMNS)]:
        require([row["column_name"] for row in metadata if row["file_name"] == filename] == columns,
                f"Schema metadata does not cover {filename} in column order")
    return {"semantic_base.csv": (MAP_COLUMNS, semantic), "field_values.csv": (VALUE_COLUMNS, values),
            "semantic_base_metadata.csv": (METADATA_COLUMNS, metadata)}


def validate(semantic, values, parameters, samples):
    keys = [(row["endpoint"], row["response_field"] or row["request_field"]) for row in semantic]
    require(len(keys) == len(set(keys)), "Duplicate endpoint/field identity")
    for endpoint, request in parameters.items():
        rows = [row for row in semantic if row["endpoint"] == endpoint]
        require({row["request_field"] for row in rows if row["request_field"]} == set(request),
                f"Request field coverage differs for {endpoint}")
        require({row["response_field"] for row in rows if row["response_field"]} == set(samples[endpoint][1]),
                f"Response field coverage differs for {endpoint}")
    dictionary = {(relative(path), field): definition
                  for (_, field), (path, definition) in dictionary_rows().items()}
    for row in semantic:
        require(row["mapping_status"] in {"verified", "inferred", "unresolved"}, "Unknown mapping status")
        require(row["mapping_evidence"], "Mapping evidence is required")
        require(bool(row["request_field"]) == bool(row["request_location"]), "Request location mismatch")
        require(bool(row["data_dictionary"]) == bool(row["data_dictionary_field"]), "Incomplete dictionary candidate")
        if row["description_source"]:
            require((EUDAMED / row["description_source"].split("#", 1)[0]).is_file(), "Missing description source")
        if row["data_dictionary"]:
            key = row["data_dictionary"], row["data_dictionary_field"]
            require(key in dictionary, f"Dictionary field does not exist: {key}")
            require(row["dictionary_enum"] == clean(dictionary[key].get("ENUM Reference Code", "")), "Dictionary enum differs from source")
            require(row["mapping_status"] != "verified", "Dictionary crosswalk not explicitly verified")
    require(len({tuple(row[column] for column in VALUE_COLUMNS) for row in values}) == len(values), "Duplicate value evidence row")
    for row in values:
        require((row["endpoint"], row["field"]) in keys, "Value has no semantic field")
        require(present(row["value"]), "Missing marker cannot be a field value")
        require(row["value_kind"] in {"observed", "allowed", "reference-listed"}, "Invalid value evidence class")
        require(row["value_scope"] in {"request", "response", "request_response", "dictionary"}, "Invalid value scope")
        require((EUDAMED / row["source"]).is_file(), "Missing value source")


# Export deterministic source-derived CSVs without changing source snapshots.
if __name__ == "__main__":
    tables = build_tables()
    for filename, (columns, records) in tables.items():
        with (BASE / filename).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(records)
        print(f"{filename}: {len(records)} rows")
    print(dict(Counter(row["mapping_status"] for row in tables["semantic_base.csv"][1])))
