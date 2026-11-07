"""Build semantic_base.csv from TED API search fields and eForms SDK metadata.

Run with Python and pandas installed. Input and output paths are relative to this
script, so it can run from any working directory. Unmatched references are kept.
"""

from pathlib import Path

import pandas as pd


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
            semantic_base / "API map" / "List_of_search_fields.csv",
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
    output_path = Path(__file__).resolve().parent / "semantic_base.csv"
    semantic_base_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(semantic_base_df)} rows to {output_path}")
