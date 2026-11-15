"""Build the TED semantic field map and its schema metadata.

Run with Python and pandas installed. Input and output paths are relative to this
script, so it can run from any working directory. Unmatched references are kept.
"""

from pathlib import Path

import pandas as pd


# Describe the actual local CSV projection, independently of the API JSON schema.
def build_semantic_base_metadata():
    metadata_columns = [
        "file_name", "column_name", "data_type", "nullable", "description",
        "source", "derivation", "allowed_values", "key_role",
    ]
    api_source = "semantic base/API/List_of_search_fields.csv"
    sdk_source = "semantic base/field semantics/CSVs download/fields.csv"
    definitions = [
        ("Search field", "string", "no", "Primary TED API search-field name, with source spelling and case preserved.",
         f"{api_source}#Search field",
         "Copied without alias expansion or case normalization; repeated when the source references several SDK fields. Not unique alone."),
        ("sdk_field_key", "string", "yes", "Normalized individual SDK reference used for the left join.",
         f"{api_source}#Reference in the eForms SDK; {sdk_source}#fieldId",
         "Trim and lowercase source reference and fieldId keys; split comma/semicolon/newline only outside brackets; explode references; remove bracketed conditions. Blank reference rows are retained; a nonblank key may still be unmatched."),
        ("btId", "string", "yes", "Business-term identifier recorded on the matched SDK implementing field.",
         f"{sdk_source}#btId",
         "Copied after a many-to-one validated join on sdk_field_key; not derived from an API field name or ID prefix. Blank when source metadata or the SDK match is missing."),
        ("type", "string", "yes", "SDK implementing-field type, such as code, indicator or text-multilingual.",
         f"{sdk_source}#type",
         "Copied from the matched source. Describes the SDK field, not the API request parameter or response JSON shape. Blank for missing source metadata or an unmatched key."),
        ("name", "string", "yes", "Descriptive SDK implementing-field name.",
         f"{sdk_source}#name",
         "Source text copied from the matched SDK field; distinct from the API search-field name and its displayed nameLabel. Blank for missing source metadata or an unmatched key."),
        ("nameLabel", "string", "yes", "English human-readable field label in the local SDK CSV snapshot.",
         f"{sdk_source}#nameLabel",
         "Copy the source label text, not a generated translation or unresolved localization key. Blank for missing source metadata or an unmatched key."),
        ("descriptionLabel", "string", "yes", "English human-readable SDK field description in the local source snapshot.",
         f"{sdk_source}#descriptionLabel",
         "Copy the source description text. It is not proof that every API alias or response projection has identical representation or constraints. Blank for missing source metadata or an unmatched key."),
        ("maxLength", "integer", "yes", "Maximum length recorded for the SDK implementing field where applicable.",
         f"{sdk_source}#maxLength",
         "Pandas default NA parsing converts source NULL markers to missing values. Nonmissing integer-valued lengths are serialized with a decimal suffix (for example 1000.0) after the nullable numeric join; missing values export as empty cells. This is not an API query/filter length limit."),
        ("businessEntityId", "string", "yes", "SDK business entity owning the matched implementing field, such as Lot or Organisation.",
         f"{sdk_source}#businessEntityId",
         "Copied from the matched SDK row; not inferred solely from suffixes in the API field name. Blank for missing source metadata or an unmatched key."),
    ]
    rows = []
    for column, data_type, nullable, description, source, derivation in definitions:
        key_role = ""
        if column in {"Search field", "sdk_field_key"}:
            key_role = "row grain: search field plus parsed SDK reference; uniqueness is not enforced by the builder"
        rows.append(["semantic_base.csv", column, data_type, nullable, description, source,
                     derivation, "", key_role])
    return pd.DataFrame(rows, columns=metadata_columns)


# Split multiple SDK references without splitting inside bracketed conditions.
def split_sdk_references(reference):
    if pd.isna(reference):
        return [pd.NA]
    references = []
    current = []
    depth = 0
    for character in reference:
        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
        if character in ",;\r\n" and depth == 0:
            if "".join(current).strip():
                references.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    if "".join(current).strip():
        references.append("".join(current).strip())
    return references or [pd.NA]


def build_semantic_base(api_search_fields_df=None, bs_fields_df=None):
    """Join supplied source dataframes, or load the source CSVs when omitted.

    Accept original CSV column names or the exploration notebook's renamed IDs.
    Supplied dataframes are copied before normalization.
    """
    semantic_base = Path(__file__).resolve().parent
    field_columns = [
        "fieldId", "btId", "type", "name", "nameLabel", "descriptionLabel",
        "maxLength", "businessEntityId",
    ]

    # Load only inputs that were not supplied by the caller.
    if api_search_fields_df is None:
        api_search_fields_df = pd.read_csv(
            semantic_base / "API" / "List_of_search_fields.csv",
            usecols=["Search field", "Reference in the eForms SDK"],
            encoding="utf-8-sig",
        )
    if bs_fields_df is None:
        bs_fields_df = pd.read_csv(
            semantic_base / "field semantics" / "CSVs download" / "fields.csv",
            usecols=field_columns,
            encoding="utf-8-sig",
        )

    # Use the same source columns for CSV inputs and preloaded notebook dataframes.
    api_search_fields_df = api_search_fields_df.rename(columns={
        "api_field_id": "Search field",
        "sdk_field_id": "sdk_field",
        "Reference in the eForms SDK": "sdk_field",
    })[["Search field", "sdk_field"]].copy()
    bs_fields_df = bs_fields_df.rename(columns={
        "sdk_field_id": "fieldId", "bs_term_id": "btId",
    })[field_columns]
    bs_fields_df = bs_fields_df[
        bs_fields_df["fieldId"].notna() & bs_fields_df["fieldId"].ne("")
    ].copy()

    # Normalize join keys while preserving search-field names and SDK metadata.
    for frame, column in (
        (api_search_fields_df, "sdk_field"),
        (bs_fields_df, "fieldId"),
    ):
        frame["sdk_field_key"] = frame[column].astype("string").str.strip().str.lower()

    # Convert each reference string into a list, splitting only outside brackets.
    api_search_fields_df["sdk_field_key"] = api_search_fields_df["sdk_field_key"].map(split_sdk_references)
    # Create one row per reference, repeating the search-field name and resetting the index.
    api_search_fields_df = api_search_fields_df.explode("sdk_field_key", ignore_index=True)
    # Preserve missing values, keep the text before the first bracket, and trim whitespace.
    api_search_fields_df["sdk_field_key"] = (
        api_search_fields_df["sdk_field_key"].astype("string")
        .str.split("[", n=1, regex=False).str[0].str.strip()
    )
    # Remove the original reference text now that individual join keys are available.
    api_search_fields_df = api_search_fields_df.drop(columns="sdk_field")

    # The normalized SDK key already identifies the field in the joined output.
    bs_fields_df = bs_fields_df.drop(columns="fieldId")

    # Keep all API search references and validate that each SDK key has at most one match.
    return api_search_fields_df.merge(
        bs_fields_df,
        on="sdk_field_key",
        how="left",
        validate="many_to_one",
    )


# Export the joined table without a dataframe index.
if __name__ == "__main__":
    semantic_base_df = build_semantic_base()
    metadata_df = build_semantic_base_metadata()
    if metadata_df["column_name"].tolist() != semantic_base_df.columns.tolist():
        raise ValueError("Schema metadata does not match semantic_base.csv columns")
    for filename, frame in [("semantic_base.csv", semantic_base_df),
                            ("semantic_base_metadata.csv", metadata_df)]:
        output_path = Path(__file__).resolve().parent / filename
        frame.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"Wrote {len(frame)} rows to {output_path}")
