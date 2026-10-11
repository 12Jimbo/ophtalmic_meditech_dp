---
name: context_edge_manager
description: creates or updates connections between context_node.md files in the project
---

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
    - If file_y does not have a CNT record, create it
    - If assumptions are met, file_x path is added to the female, unless already present
- Cut the edge from file_x to file_y on field_z:
    - If assumptions are met, file_x path is removed from the female, if present
- Regrow the edge from file_x to file_y on field_z:
    - The instruction assumes that file_x old path is listed in the female, but file_x new path is not
    - If assumptions are met:
        - cut the edge from file_x to file_y on field_z using the old file_x path
        - grow the edge from file_x to file_y on field_z using the new file_x path