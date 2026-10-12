---
name: context_node_manager
description: creates or updates context_node.md files in the project
---

Read the context_node_master `.claude/context_grid/context_node_master.md`.
Invoke the contect_edge_manager `.claude/context_grid/context_edge_manager.md` when operating on edges.

The process described in this document is meant to have as object a file_x in folder_x, for x in [1, ... n]. 

FOR EACH FILE_X, FOLLOW THE NODE UPDATE PROCESS
------------------------------------------------------------------------------------------------------
It is assumed that:
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
    - If no context_node.md file exists in folder_x, create it
    - Read the context_node_master.md field rules to inform how you assign values each field in the following process
    - Update the CNT schema, if it does match the fields described in the context node master:
        - Add all new master fields to the CNT, initializing to empty for each record
        - Remove all master fields in CNT that are not in the context node master 
    - Create or update the record for file_x in the CNT of context_node.md

- Whenever you create a context_node.md file in folder_x, use context_node_master as template:
    - Copy from template only table schemas and table titles
    - Add in the first line a reference to the master filepath, indicating the timestamp of master last commit

- Whenever you create the CNT record of file_x in a context_node.md:
    - Read file_x and it's context node CNT
    - Assign a value to each field in the file_x record, as prescribed by the field rules
    

- Whenever you delete the CNT record of file_x in a context_node.md:
    - For each male vertex in file_x record, for each file_y path in the male vertex, cut the edge from file_x to file_y on the male vertex
    - Remove file_x CNT record

- Whenever you update the CNT record of file_x in the CNT of a context_node.md:
    - Keep in memory the old version of the CNT record for the duration of the session
    - Refresh the timestamp of last master commit in context_node.md
    - Following the field rules, update, in this order:
        - The `resource` field 
        - simple fields
        - male vertexes

------------------------------------------------------------------------------------------------------

After node processing has executed for each file_x, call the context edge manager and pass it for edge processing:
 - created_records_list: the list of resources for which a CNT record was created during the present process: 
 - updated_ids_list: the list of resources for which the CNT record id was updated during the present process: 
 - updated_males_list: the list of resources for which CNT record male vertexes were updated during the present process. For each male vertex, provide the sublists:
    - Of resources that were added to the vertex
    - Of resources taht were removed from the present vertex

