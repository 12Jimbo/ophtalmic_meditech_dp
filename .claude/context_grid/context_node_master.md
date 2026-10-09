
-- MASTER CONTEXT NODE TEMPLATE
-- This document serves as template for context_node.md files, aka context nodes.
-- This document also specifies how to instantiate context node from this template - how to fill placeholders with actual values.
-- Rows beginning with "--" will be treted as comment and not be included in instances of this template
-- The expressions "current folder" or "folder" in the following will refer to the folder of the instantiated context node

# Context Node
Each context node stores metadata about files in its same folder path.
There cannot be more than one context nodes in the same folder.
Therfore, expressions like "this file's context node" unambigously refer to the context node residing in the same folder as the file in object.

# Project Grid Table (PGT)
Table description:
the project grid table tracks, for each code file (resource) in this table:
  - Code dependencies upstream and downstream
  - Data dependencies upstream and downstream

--Sample PGT:
| resource | description | imports_from | imported_by | sources | targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `scripts\clean_data.py` | Cleans the raw dataset for downstream analysis. | [`config\settings.py`] | [`notebooks\analysis.ipynb`] | [`data\raw.csv`] | [`data\clean.csv`] | `2026-10-08T08:34:00+02:00` | 1 |


Field Rules:
  - resource: is the path relative to project root of a file in the current folder, serves as record id. 
    - resource path cannot be empty or null
    - There cannot be duplicates of this field in the PGT for a given context node file.
    - Expressions like "this file's PGT record" unambigously refer to the record in the PGT of the file's context node identified by the file's path
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
    - can propagate to `imported_by`
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

Field Rule Concepts:
  - Propagating fields: fields that can propagate to a target field are able to reference a target file, and iform updates to the target field of the referenced file PGT record.
    - There can be more than one target file
    - There can be more than one target field
    - Target files can reside in locations different than the current node's location