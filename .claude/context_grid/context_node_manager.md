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
    - If file_x has been deleted, and has CNT record:
        - Propagate:
            - `imports_from` to `imported_by`: in each CNT record of each file in `imports_from`, remove file_x path from `imported_by`
        - Remove file_x CNT record
        - End of processing

    - Otherwise, check whether a context_node.md file is present in folder_x. Then:
        - If no context_node.md file exists in folder_x:
            - create a context_node.md file in folder_x using context_node_master as template
                - Do not copy from template rows beginning with "--"
        - Read the context_node.md field rules to inform how you assign values each field in the following process
        - Create or update the record for file_x in the CNT of context_node.md

- Whenever you create a record in the CNT of a context_node.md for file_x:
    - Read file_x 
    - Assign a value to each field in the file_x record, as prescribed by the field rules. 
    - Propagate `imports_from` to `imported_by`: for each CNT record of each file_y in `imports_from`:
        - If file_y does not have a context node, create a context node for file_y 
        - If file_y does not have a CNT record, create a CNT record for file_y
        - if the path to file_x is not in `imported_by`, add it to `imported_by` 

- Whenever you update the record of file_x in the CNT of a context_node.md:
    - Consider the edits you made to file_x, and your knowledge regarding file_x already available to the present session
    - If file_x has been moved or renamed:
        - Update file_x `resource` value in its CNT record
        - Reverse propagate:
            - `imports_from` to `imported_by`: for each CNT record of each file in `imported_by`, remove file_x path from `imports_from`, and add file_x new path
    -  If file_x content was edited:
        - Update all non propagating fields in the file_x CNT record as prescribed by the field rules.
        - If field rules prescribe updating of propagating fields:
            - Take a session lasting note of the present field value: prop_f_old
            - Take a session lasting note of the updated field value: prop_f_new
            - Propagate `imports_from` to `imported_by`: 
                for each file_y in prop_f_old that is not in prop_f_new:
                - If file_y does not have a context node, create a context node for file_y
                - If file_y does not have a CNT record, create a CNT record for file_y
                - Remove all copies of file_x path from `imported_by`
                for each file_y in prop_f_new:
                - If file_y does not have a context node, create a context node for file_y 
                - If file_y does not have a CNT record, create a CNT record for file_y
                - If the path to file_x is not in `imported_by`, add it to `imported_by`
            - Update propagating fields as prescribed by field rules.