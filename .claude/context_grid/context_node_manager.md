---
name: context_node_manager
description: creates, deletes, or updates context_node.md files in the project
---

Consider the context_node_master `.claude/context_grid/context_node_master.md`.

Given file_x in folder_x, the following operates under the assumption that file_x is a file containing executable code (like python or sql scripts, or notebooks). If the file does not contain executable code, halt the process and signal the discrepancy. Otherwise:

- Check whether a context_node.md file is present in folder_x. Then:
    - If no context_node.md file exists in folder_x:
        - create a context_node.md file in folder_x using context_node_master as template
        - create a record in the PGT of context_node.md for file_x
    - If a context_node.md file exists in folder_x: 
        - Create or update the record for file_x in the PGT of context_node.md

- Whenever you create a record in the PGT of a context_node.md for file_x:
    - Read the context_node.md field rules to inform how you assign values each field
    - Read file_x 
    - Assign a value to each field in the file_x record in conformity with context_node.md field rules. Don't assign or change value to the `imported_by` field at this stage.
    - Do a forward import propagation

- Whenever you update the record of file_x in the PGT of a context_node.md:
    - Read the context_node.md field rules to inform how you assign values each field
    - Consider the edits you made to file_x
    - Update each field in the file_x PGT record to keep it updated with the edits, and preserve conformity with the context_node.md field rules. Don't assign or change value to the `imported_by` field at this stage.
        - refresh `updated_at`
        - increment `update_n` by 1
    - If `imports_from` was updated, do a forward import propagation
    - If the file edits include deletion, renaming, or moving, then:
        - for each file_n listed in the `imports_from` field of file_x, check file_n `imported_by` list in its PGT record: 
            - If file_x has been deleted, remove it from the list
            - If file_x has been renamed or moved, update its path in the list
        - for each file_n listed in the `imported_by` field of file_x, check file_n `imports_from` list in its PGT record: 
            - If file_x has been deleted, remove it from the list
            - If file_x has been renamed or moved, update its path in the list
        - if the file was deleted, remove its record from its PGT

- Whenever you do a forward import propagation for file_x:
    - Consider paths that were edited, added, or removed from the `imports_from` list of the PGT record of file_x during the current process
    - For each file_n listed in the `imports_from` field of file_x, check whether file_n has a context_node.md in its folder, with a record in the PGT for file_n:
        - (expect each file_n to contain executable code as well)
        - if there is no context_node.md for file_n, create it
        - if there is no PGT record for file_n in its context_node.md create it
        - in the PGT record of file_n, add file_x to the list in the `imported_by` fields if not already present
    - For each file_n removed from the `imports_from` list of file_x, remove file_x from the `imported_by` list of file_n

