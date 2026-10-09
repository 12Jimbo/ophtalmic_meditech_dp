# Elaboration
- Evaluate the complexity of your task:
    - Consider asking the user to switch to higher effort
    - Consider asking for approval to spawn more advanced models

# Coding Style
- Include code features that were not explicitly asked for only if you deem them strictly necessary
- Try to keep the code human understandable
- Divide the code into sections, and add concise 1 line comments in the code to explain the function of each code section. Avoid comment redundancy.
- Add concise 1 line comments in the code to explain the working of code subsections when you deem it not obvious by words used in the code or too complex for average human developers.
- DRY: do not repeat yourself. If two chunks of code in a file define very similar processing logic, modularize the logic into a single function.

# Project Navigation
Whenever you access a folder as part of a task, if the folder contains a context_node.md, include context_node.md in your current session context.

context_node.md files are a fast way to acquire information about:
  - Code dependencies between project files
  - Which project files write to which data assets
  - Which project files read from which data assets
  - Data assets lineage
So reading the context_node.md might efficiently inform your decisions about which project files are worth reading, and with which priority.

# Editing and Commits
- When a task requires file editing, propose a plan in steps.
- When editing code, always consider editing documentation files to keep them coherent with the edited code
- Whenever you edit code files (like SQL or Python notebooks and scripts) in file_x, in folder_x, follow `.claude/context_grid/context_node_manager.md` to create or update the folder's context_node metadata.
- Step edits will be human reviewed in Source Control as changes, and manually staged
- If you are asked to stage changes, write a commit message in the dedicated text box under Source Control. If that is not possible, print out your suggested commit message.
- Staged changes will either be executed by the user, or by the agent after explicit user permission
- The human user will intend each step in the plan as a potential commit


# Do NOT
- Do not stage changes without explicit approval.
- Do not commit without explicit approval.
- Do not create or switch branch without explicit approval.
- Do not push or pull code without explicit approval.
- Do not rebase branch without explicit approval.
- Do not create folders in the project without explicit approval.
- Do not move files or folders to or from folders without explicit approval.
- Do not rename or delete files or folders without explicit approval.



