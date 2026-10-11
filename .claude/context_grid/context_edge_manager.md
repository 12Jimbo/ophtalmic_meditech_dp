---
name: context_edge_manager
description: creates or updates connections between context_node.md files in the project
---

The context edge manager expects to work on the context provided by the context node manager `.claude\context_grid\context_node_manager.md` upon its call. The callm from the context node manager will include several resource lists.

Semantics
- An edge from file_x to file_y on male vertex mv exists if:
    - mv is coupled with fv
    - file_x.mv is lists file_y path
    - file_y.fv lists file_x path

Assumptions
- If an instruction applies to an edge from file_x to file_y on field_z, then:
    - The instruction assumes that field_z is a male vertex coupled with a female vertex
    - For the scope of the instruction:
        - the couple's male vertex in file_x CNT record is referred to just as male
        - the couple's female vertex in file_y CNT record is referred to just as female
    - The instruction assumes that file_y path is listed in the male (the edge growth stops otherwise)

Callable Commands
- Grow an edge from file_x to file_y on field_z:
    - If file_y does not have a context node, create it
    - If file_y does not have a CNT record, create it. Override the record creation process described in the context node manager: initialize to empty all fields except for id. Then move to the step below after initialization.
    - If assumptions are met, file_x path is added to the female, unless already present
- Cut the edge from file_x to file_y on field_z:
    - If assumptions are met, file_x path is removed from the female, if present
- Regrow the edge from file_x to file_y on field_z:
    - The instruction assumes that file_x old path is listed in the female, but file_x new path is not
    - If assumptions are met:
        - cut the edge from file_x to file_y on field_z using the old file_x path
        - grow the edge from file_x to file_y on field_z using the new file_x path




EGE PROCESSING  
-----------------------------------------------------------------------------
- For each resource in updated_records_list:
    - For each male vertex, for each file_y path in it, grow the edge from file_x to file_y on the male vertex

- For each resource in updated_ids_list:
    - For each male vertex, for each file_y path in it, regrow the edge from file_x to file_y on the male vertex
    - For each female vertex and its coupled male vertex, for each file_y path in the female vertex:
        - Take note of the list of resources in the female vertex
        - Empty the female vertex
        - For each file_y path in the noted resources, grow the edge file_y to file_x on the male vertex

- For each resource in the updated_males_list:
    - For each male vertex, for each file_y path added to the male vertex, grow the edge from file_x to file_y on the male vertex
    - For each male vertex, for each file_y path removed from a male vertex, cut the edge from file_x to file_y on the male vertex


-----------------------------------------------------------------------------


