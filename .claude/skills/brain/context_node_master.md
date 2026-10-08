
-- this is a template: current folder will vary for each instance--

# Project Grid Table (PGT)
Table description:
the project grid table tracks, for each code file (resource) in this table:
  - Code dependencies upstream and downstream
  - Data dependencies upstream and downstream

Field Rules:
  - resource: is the path of a file in the current folder, serves as record id. There cannot be duplicates of this field in the PGT for a given context node file.
  - description: a summary description of the resource
    - under 150 characters
    - can be empty
    - must be assigned a value based exclusively on resource content
  - imports_from: is the list of paths relative to project root of all and only the scripts or notebooks that are imported by the resource.
    - must be assigned a value based exclusively on resource code content
    - can be empty
    - the list cannot contain duplicates
    - assign value based exclusively on resource content
    - cannot include the path in `resource` in the list
  - imported_by: is the list of paths relative to project root of scripts or notebooks that import the resource
    - can be empty
    - the list cannot contain duplicates
    - cannot include the path in `resource` in the list
  - sources: is the list of all and only the files the resource reads from
    - must be assigned a value based exclusively on resource code content
    - can be empty
    - the list cannot contain duplicates
  - targets: is the list of all and only the files the resource writes to
    - must be assigned a value based exclusively on resource code content
    - can be empty
    - the list cannot contain duplicates
  - updated_at: is the current timestamp at the time of record creation or update
  - update_n: starts at 1 upon record creation, and increases by 1 every time the record is updated
  

Sample PGT:

| resource | description | imports_from | imported_by | sources | targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `scripts\clean_data.py` | Cleans the raw dataset for downstream analysis. | [`config\settings.py`] | [`notebooks\analysis.ipynb`] | [`data\raw.csv`] | [`data\clean.csv`] | `2026-10-08T08:34:00+02:00` | 1 |
