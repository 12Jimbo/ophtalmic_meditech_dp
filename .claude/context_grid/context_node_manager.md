---
name: context_node_manager
description: creates or updates context_node.md files in the project
---

Read the context_node_master `.claude/context_grid/context_node_master.md`.
Invoke the contect_edge_manager `.claude/context_grid/context_edge_manager.md` when operating on edges.

The process described in this document is meant to have as object a file_x in folder_x, and assumes that:
    - file_x is a file containing executable code (like python or sql scripts, or notebooks)
    - file_x either has unstaged changes or has been created after the last commit
If the assumptions are not met, halt the process and signal the discrepancy. Otherwise:
- Consider file_x content, and its unstaged working-tree diff if it exists
    - If file_x has been deleted:
        - If file_x has no CNT record, stop processing file_X
        - If file_x has a CNT record:
            - Delete file_x CNT record
            - End of processing for file_x
    - If file_x has been moved from folder_z to folder_x:
        - If file_x has a CNT record in folder_z context node, delete its CNT record   
    - If no context_node.md file exists in folder_x:
        - create a context_node.md file in folder_x using context_node_master as template.
            - Copy from template only table schemas and table titles
            - Add in the first line a reference to the maste filepath
    - Read the context_node.md field rules to inform how you assign values each field in the following process
    - Create or update the record for file_x in the CNT of context_node.md

- Whenever you create the CNT record of file_x in a context_node.md:
    - Read file_x 
    - Assign a value to each field in the file_x record, as prescribed by the field rules. 
    - For each male vertex, for each file_y path in it, grow the edge from file_x to file_y on the male vertex

- Whenever you delete the CNT record of file_x in a context_node.md:
    - For each male vertex in file_x record, for each file_y path in the male vertex, cut the edge from file_x to file_y on the male vertex
    - Remove file_x CNT record

- Whenever you update the CNT record of file_x in the CNT of a context_node.md:
    - Keep in memory the old version of the CNT record for the duration of the session
    - If file_x has been renamed:
        - Update file_x `resource` value in its CNT record with the new file_x path
        - For each male vertex, for each file_y path in it, regrow the edge from file_x to file_y on the male vertex
        - For each female vertex and its coupled male vertex, for each file_y path in the female vertex:
            - Take note of the list of resources in the female vertex
            - Empty the female vertex
            - For each file_y path in the noted resources, grow the edge file_y to file_x on the male vertex
    - If file_x content was edited:
        - Following the field rules, update, in this order:
            - The `resource` field 
            - simple fields
            - male vertexes
        - Then:
            - If the `resource` has changed value as result of the update, for each male vertex, for each file_y path in it, regrow the edge from file_x to file_y on the male vertex
            - Otherwise:
                - For each male vertex, for each file_y path added to the male vertex, grow the edge from file_x to file_y on the male vertex
                - For each male vertex, for each file_y path removed from a male vertex, cut the edge from file_x to file_y on the male vertex
