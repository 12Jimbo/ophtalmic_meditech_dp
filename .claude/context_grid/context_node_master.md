
-- MASTER CONTEXT NODE TEMPLATE
-- This document serves as template for context_node.md files, aka context nodes.
-- This document also specifies how to instantiate context node from this template - how to fill placeholders with actual values.
-- Rows beginning with "--" will be treated as comments and not be included in instances of this template
-- The expressions "current folder" or "folder" in the following will refer to the folder of the instantiated context node

# Context Node
Each context node stores metadata about files in its same folder path.
There cannot be more than one context node in the same folder.
Therefore, expressions like "this file's context node" unambiguously refer to the context node residing in the same folder as the file in question.

# Code Node Table (CNT)
Table description:
the code node table tracks, for each code file (resource) in this table:
  - Code dependencies upstream and downstream
  - Data dependencies upstream and downstream

--Sample CNT:
| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `scripts\clean_data.py` | Cleans the raw dataset for downstream analysis. | [`config\settings.py`] | [`notebooks\analysis.ipynb`] | [`data\raw.csv`] | [`data\clean.csv`] | `2026-10-08T08:34:00+02:00` | 1 |


Field Rules:
  - `resource`: is the path relative to project root of a file in the current folder, serves as record id. 
    - resource path cannot be empty or null
    - There cannot be duplicates of this field in the CNT for a given context node file.
    - Expressions like "this file's CNT record" unambiguously refer to the record in the CNT of the file's context node identified by the file's path
  - `description`: a summary description of the resource
    - under 150 characters
    - can be empty
    - must be assigned a value based exclusively on resource content
  - `imports_from`: is the list of paths relative to project root of all and only the scripts or notebooks that are imported by the resource.
    - is a male vertex to `imported_by`
    - must be assigned a value based exclusively on resource code content
    - cannot include the path in the `resource` field of the record
    - can propagate to `imported_by`
  - `imported_by`: is the list of paths relative to project root of scripts or notebooks that import the resource
    - is a female vertex to CNT `importt_from`
    - can be populated only as target of a propagating fied
  - `data_sources`: is the list of all and only the files the resource reads from
    - is a vertex
    - must be assigned a value based exclusively on resource code content
  - `data_targets`: is the list of all and only the files the resource writes to
    - is a vertex
    - must be assigned a value based exclusively on resource code content
  - `updated_at`: is the current timestamp at the time of record creation or update
  - `update_n`: starts at 1 upon record creation, and increases by 1 every time the record is updated

Grid Rules:
  - Vertex fields:
    - Are a lists of file paths relative to project root
    - Vertexes can be empty
    - Vertexes can't contain duplicates
    - Vertexes cannot include the path in the `resource` field of the same record
    - Vertex fields can be:
      - Female, relative to a given male vertex field of a node table
        - Upon record creation, female vertexes are initialized to empty
      - Male, relative to a given female vertex field of a node table
        - Upon record creation, for each file path listed in the male vertex, add the male's `resource` value to that file's female vertex if it exists
    - Two vertex fields are considered coupled if they are male and female relative to each other
