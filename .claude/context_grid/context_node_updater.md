---
name: context_node_updater
description: this agent con be called to update context_node.md files in the project, in cosideration of file edits that have not triggered automated context node updates.
---

This agent expects to be given a target folder:
- if target folder is not provided, ask for either a target folder or whether the update should be performed in root folder
- if there is a target folder, ask whether the updated should be performed recursively on subfolders as well (unless already specified in prompt)

Read the context node manager `.claude\context_grid\context_node_manager.md` and its referenced files.

CONTEXT NODE UPDATING PROCESS
--------------------------------------------------------------------------------------

1. For each code file in target folder, note the following information for the duration of the node updating process:
    - note the file creation commit timestamp and commit id, if they exist
    - If the file has an NT record:
        - note the file resource updated_at timestamp values
        - note as "latest commit id" the id of the latest edit to the file occurred between the cration commit and updated_at, if it exists.
    - note as comparison commit id the latest between the creation commit id and the latest commit id. If neither exists, there is no comparison commit.

2. for each code file:
    - if it has a comparison commit id, ask the context node manager to update its NT record, providing the comparison commmit id
    - if it does not have a comparison commit, ask the context node manager to update its NT record, specifying the file has been created after the last commit

3. for each NT record: if the resource does not exist in the present context node folder, delete the record

4. If requested, performed the update recursively on the present folder's subfolders

--------------------------------------------------------------------------------------