---
name: context_node_manager
description: creates, deletes, or updates context_node.md files in the project
---

Read the context_node_master `.claude/context_grid/context_node_master.md`.

Given file_x in folder_x, the following operates under the assumption that file_x is a file containing executable code (like python or sql scripts, or notebooks). If the file does not contain executable code, halt the process and signal the discrepancy. Otherwise:

- Check whether a context_node.md file is present in folder_x. Then:
    - If no context_node.md file exists in folder_x:
        - create a context_node.md file in folder_x using context_node_master as template
            - Do not copy from template rows beginning with "--"
    - Read the context_node.md field rules to inform how you assign values each field in the following process
    - Create or update the record for file_x in the PGT of context_node.md

- Whenever you create a record in the PGT of a context_node.md for file_x:
    - Read file_x 
    - Assign a value to fields in the file_x record, as prescribed by the field rules. 
    - Propagate:
        - `imports_from` to `imported_by`: 
            for each file_n in the `imports_from` list:
            - let's name x_imports_from = current `imports_from` list
            - If file_y does not have a context node, create a contex node for file_y (and consequently its PGT record)
            - let's name y_imported_by = the `imported_by` list of file_'s PGT record
            - If the path to file_x is not in y_imported_by, add it to y_imported_by

- Whenever you update the record of file_x in the PGT of a context_node.md:
    - Consider the edits you made to file_x, and your knowledge regarding file_x already available to the present session
    - If file_x has been deleted:
        - Propagate:
            - `imports_from` to `imported_by`: for each PGT record of each file in `imports_from`, remove file_x path from `imported_by`
        - Remove file_x PGT record
    - If file_x has been moved or renamed:
        - Propagate:
            - `imports_from` to `imported_by`: for each PGT record of each file in `imports_from`, remove file_x path from `imported_by`, and add file_x new path
    -  If file_x content was edited:
        - Update all non propagating fields in the file_x PGT record as prescribed by the field rules.
        - If any propagating field requires updating to preserve conformity with the field rules:
            - Take a session lasting note of the present field value: prop_f_old
            - Take a session lasting note of the updated field value: prop_f_new
            - Propagate:
                - `imports_from` to `imported_by`: 
                    for each file_n in prop_f_old that is not in prop_f_new:
                    - If file_y does not have a context node, create a contex node for file_y (and consequently its PGT record)
                    - let's name y_imported_by = the `imported_by` list of file_'s PGT record
                    - Remove all copies of file_x path from y_imported_by
                    for each file_n in prop_f_new:
                    - If file_y does not have a context node, create a contex node for file_y (and consequently its PGT record)
                    - let's name y_imported_by = the `imported_by` list of file_'s PGT record
                    - If the path to file_x is not in y_imported_by, add it to y_imported_by