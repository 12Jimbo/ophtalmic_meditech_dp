
MASTER CONTEXT NODE TEMPLATE
This document serves as template for context_node.md files, aka context nodes.
This document also specifies how to instantiate context node from this template - how to fill placeholders with actual values.
The expressions "current folder" or "folder" in the following will refer to the folder of the instantiated context node

# Context Node
Each context node stores metadata about files in its same folder path.
There cannot be more than one context node in the same folder.
Therefore, expressions like "this file's context node" unambiguously refer to the context node residing in the same folder as the file in question.

# Code Node Table (CNT)
Table description:
the code node table tracks, for each code file (resource) in this table:
  - Code dependencies upstream and downstream
  - Data dependencies upstream and downstream

Code Node Table (CNT) - Sample
| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `scripts\clean_data.py` | Cleans the raw dataset for downstream analysis. | [`config\settings.py`] | [`notebooks\analysis.ipynb`] | [`data\raw.csv`] | [`data\clean.csv`] | `2026-10-08T08:34:00+02:00` | 1 |


Field Rules:
  - `resource`: is the path relative to project root of a file in the current folder
    - is the record id. 
    - Expressions like "this file's CNT record" unambiguously refer to the record in the CNT of the file's context node identified by the file's path
    - In the context of context nodes, the term "resource" refers to a file paths relative to project root
  - `description`: a summary description of the resource
    - under 150 characters
    - can be empty
    - must be assigned a value based exclusively on resource content
  - `imports_from`: is the list of resources of all and only the scripts or notebooks that are imported by the resource.
    - is a male vertex coupled with CNT `imported_by`
  - `imported_by`: is the list of resources of scripts or notebooks that import the resource
    - is a female vertex coupled with CNT `imports_from`
  - `data_sources`: is the list of all and only the files the resource reads from
    - is a vertex
  - `data_targets`: is the list of all and only the files the resource writes to
    - is a vertex
  - `updated_at`: is the current timestamp at the time of record creation or update
  - `update_n`: starts at 1 upon record creation, and increases by 1 every time the record is updated

By convention, fields that evaluate to empty string have never been processed.
Fields that evaluate to NONE have been processed, but it was found there is no value to assigned them.

Field types:
  - Simple fields: if a field has no specified type, it's assumed to be a simple field

  - Record identity field, aka record id. An id field value:
    - cannot be empty 
    - cannot be null
    - must be unique in the table
    - there can be only one id field per table
  - Vertex fields:
    - Are a lists of file resources
    - Vertexes can be empty strings
    - Vertexes initialize to empty lists []
    - Vertexes can't contain duplicates
    - Vertexes cannot include the resource that identifies their own record
    - Vertex fields can be coupled:
      - As females, to a given male vertex field of a node table
        - Upon record creation, female vertexes are initialized to empty
        - Has to be coupled to one and only one male vertex
        - Female vertexes are reciprocal indexes derived from males
      - As males, relative to a given female vertex field of a node table
        - Has to be coupled to one and only one female vertex
        - Males are authoritative and are assigned values based on resource code exclusively

  - Metadata Fields
    - Metadata fields describe events of resource content editing
    - Metadata fields are not refreshed when their CNT record is edited exclusively in the `resource` field or in female vertexes
