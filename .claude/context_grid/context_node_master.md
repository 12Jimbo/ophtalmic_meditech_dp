
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
Code files can be recorded in CNT to extract from their code, and track, information about:
  - Upstream and downstream code dependencies
  - Data sources
  - Data targets
  - General description of the code

Code Node Table (CNT) - Sample
| resource | description | imports_from | imported_by | data_sources | data_targets | updated_at | update_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `scripts\clean_data.py` | Cleans the raw dataset for downstream analysis. | [`config\settings.py`] | [`notebooks\analysis.ipynb`] | [`data\raw.csv`] | [`data\clean.csv`] | `2026-10-08T08:34:00+02:00` | 1 |


### CNT Field Rules:
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
    - is a male vertex coupled with DNT `readers`
  - `data_targets`: is the list of all and only the files the resource writes to
    - is a male vertex coupled with DNT `writers`
  - `updated_at`: is the current timestamp at the time of record creation or update
  - `update_n`: starts at 1 upon record creation, and increases by 1 every time the record is updated

  - Metadata Fields
    - Metadata fields describe events of resource content editing
    - Metadata fields are not refreshed when their CNT record is edited exclusively in the `resource` field or in female vertexes

# Data Node Table (DNT)
Table description:
Data files can be recorded in DNT to keep track of which code files use them as sources, and which as targets.

Data Node Table (DNT) - Sample
| resource | writers | readers |
| --- | --- | --- |
| `data\source_1.csv` | [`config\settings.py`] | [`notebooks\analysis.ipynb`]

### DNT Field Rules:
  - `resource`:  is the path relative to project root of a file in the current folder
    - is the record id. 
    - Expressions like "this file's DNT record" unambiguously refer to the record in the DNT of the file's context node identified by the file's path
    - In the context of context nodes, the term "resource" refers to a file paths relative to project root
  - `readers`: the list of code files that can read data from the resource
    - is a female vertex coupled with CNT `data_sources`
  - `writers`: the list of code files that can write data to the resource
    - is a female vertex coupled with CNT `data_targets`


# Field types:
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