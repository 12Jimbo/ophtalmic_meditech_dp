---
name: context_node_manager
description: creates, deletes, or updates context_node.md files in the project
---

Read the context_node_master `.claude/context_grid/context_node_master.md`.

The process described in this document is meant to have as object a file_x in folder_x, and assumes that:
    - file_x is a file containing executable code (like python or sql scripts, or notebooks)
    - file_x has unstaged changes
If the assumptions are not met, halt the process and signal the discrepancy. Otherwise:
- Consider file_x diff
    - If file_x has been deleted, and has a CNT record:
        - For each male vertex in file_x record, for each file_y path in the male vertex, cut the file_y edge originating from file_x male vertex
        - Remove file_x CNT record
        - End of processing for file_x
    - Otherwise:
        - If no context_node.md file exists in folder_x:
            - create a context_node.md file in folder_x using context_node_master as template
                - Do not copy from template rows beginning with "--"
        - Read the context_node.md field rules to inform how you assign values each field in the following process
        - Create or update the record for file_x in the CNT of context_node.md

- Whenever you create a CNT record of file_x in a context_node.md:
    - Read file_x 
    - Assign a value to each field in the file_x record, as prescribed by the field rules. 
    - For each male vertex field, for each file_y path in male_vertex_z, grow the edge from file_x to file_y on the male vertex field

- Whenever you update the record of file_x in the CNT of a context_node.md:
    - Consider file_x diff
    - If file_x has been moved or renamed:
        - Update file_x `resource` value in its CNT record with the new file_x path
        - For each male vertex, for each file_y path in male_vertex_z, regrow the edge from file_x to file_y on the male vertex
    - If file_x content was edited:
        - Update all non female vertex fields in the file_x CNT record as prescribed by the field rules.
        - For each male vertex, for each file_y path added to the male vertex, grow the edge from file_x to file_y on the male vertex
        - For each male vertex, for each file_y path removed from a male vertex, cut the edge from file_x to file_y on the male vertex

Grid management commands:
    - "There is and edge from file_x male vertex to file_y" means that a given male vertex of file_x lists file_y, and that the coupled female vertex of file_y lists file_x `resource` value
    - If an instruction applies to an edge from file_x to file_y on field_z, then:
        - The instruction assumes that field_z is a coupled vertex, 
        - For the scope of the instruction:
            - the couple's male vertex in file_x CTN record is referred to just as male
            - the couple's female vertex in file_y CTN record is referred to just as female
        - The instruction assumes that file_y path is listed in the male (the edge growth stops otherwise)
    - If invoking: grow an edge from file_x to file_y on field_z:
        - If assumptions are met, file_x path is added to the female (unless already present)
    - If invoking: cut the edge from file_x to file_y on field_z:
        - The instruction assumes file_x path is listed in the female        
        - If assumptions are met, file_x path is removed from the female
    - If invoking: regrow the edge from file_x to file_y on field_z:
        - The instruction assumes that file_x old path is listed in the female, but file_x new path is not
        - If assumptions are met:
            - cut the edge from file_x to file_y on field_z using the old file_x path
            - grow the edge from file_x to file_y on field_z using the new file_x path
    
  
