---
name: context_node_manager
description: creates, deletes, or updates context_node.md files in the project
---

Read the context_node_master `.claude/context_grid/context_node_master.md`.

The process described in this document is meant to have as object a file_x in folder_x, and assumes that:
    - file_x is a file containing executable code (like python or sql scripts, or notebooks)
    - file_x has unstaged changes
If the assumptions are not met, halt the process and signal the discrepancy. 
Otherwise:
- Start by considering file_x staged changes:
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

- Whenever you create a record in the CNT of a context_node.md for file_x:
    - Read file_x 
    - Assign a value to each field in the file_x record, as prescribed by the field rules. 
    - For each male vertex field, for each file_y path in the male vertex, grow file_y edge from file_x male vertex

- Whenever you update the record of file_x in the CNT of a context_node.md:
    - Consider the edits you made to file_x, and your knowledge regarding file_x already available to the present session
    - If file_x has been moved or renamed:
        - Update file_x `resource` value in its CNT record
        - For each male vertex, for each file_y path in the male vertex, regrow file_y edge from file_x male vertex
    -  If file_x content was edited:
        - Update all non female vertex fields in the file_x CNT record as prescribed by the field rules.
        - For each file_y path added to a male vertex, grow file_y edge from file_x male vertex
        - For each file_y path removed from a male vertex, cut file_y edge from file_x male vertex

Grid management commands:
    - "There is and edge from file_x male vertex to file_y" means that a given male vertex of file_x lists file_y, and that the coupled female vertex of file_y lists file_x `resource` value
    - If invoking: grow file_y edge from file_x male vertex:
        - The instruction assumes file_y path is in the given male vertex of file_x (the edge growth stops otherwise)
        - The instruction assumes file_y CTN has the female vertex coupled with the given male vertex (the edge growth stops otherwise)
        - If assumptions are met, file_x `resource` value is added to file_y female vertex
    - If invoking: cut file_y edge originating from file_x male_vertex:
        - The instruction assumes file_y CTN has the female vertex coupled with the given male vertex (the edge growth stops otherwise)
        - If assumptions are met, file_x `resource` value is removed from file_y female vertex
    - If invoking: regrow file_y edge from file_x male vertex:
        - The instruction assumes there is and edge from file_x male vertex to file_y (if there isn't propose growing file_y edge from file_x male vertex instead) for the old file_x `resource` value
        - cut file_y edge originating from file_x male_vertex using the old file_x `resource` value
        - grow file_y edge from file_x male vertex using the enw file_x `resource` value
    
  
