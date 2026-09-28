# Elaboration
- Evaluate the complexity of your task:
    - Consider asking the user to switch to higher effort
    - Consider asking approval to spawn a more advanced models

# Coding Style
- Include code features that were not explicitly asked for only if you deem them strictly necessary
- Try to keep the code human understandable
- Divide the code into sections, and add concise 1 line comments in the code to explain the function of each code section. Avoid comment redundancy.
- Add concise 1 line comments in the code to explain the working of code subsections when you deem it not obvious by words used in the code or too complex for average human developers.
- DRY: do not repeat yourself. If two chunks of code in a file define very similar processing logic, modularize the logic into a single function.

# Project Navigation
When evading a task, rely on BRAIN.md and neuron.md files to inform project navigation. Assume the brain and neurons will present file descriptions and references to files, that should speed up your decision to inspect or access a file or folder, compared to actually reading the file or folder content.

# Project Brain
Expect a BRAIN.md in the project root.

- Whenever you access a folder as part of a task, if the folder contains a neuron.md, include neuron.md in your current session context.

- Whenever you edit code (like SQL or Python) in file_x, in folder_x, check whether a neuron.md file is present in folder_x. Then:
    - If no neuron.md file is present:
        - create a neuron.md file in folder_x
        - create an entry in neuron.md for file_x
    - If a neuron.md file is present in folder_x: 
        - Create or update the entry for file_x in neuron.md
        - Update tags. An file entry in neuron.md cannot have more than 10 tags. Tags can't have doubles, but if a tag is pertinent to the present task, increase by 1 its counter. 
     
- Whenever you create a neuron:
    - Structure the neuron according to the following template: a neuron is devided in 3 sections: axon, body, and dendrites
    - Determine the neuron's parent as the closest neuron.md in the current neuron's ancestor folders. If there is no parent neuron, assign BRAIN.md as parent
    - Determine the neuron's childrens as the list of closest neuron.md in each subpath of the current neuron's location. A neuron can have no chilren.
    - Add a reference to the parent neuron to the current neuron under the axon section.
    - Add a reference to the current neuron to each one of its children, under the dendrites section
    - Update the parent neuron reference in each child of the current neuron, to reference the current neuron. There can be only one parent for each neuron.

- Whenever you create an entry in a neuron.md for file_x:
    - create the entry under the body section of the neuron
    - the entry has the following fields, assign a value to each:
        - file: a reference to file_x
        - description: a summary description of file_x functionalities, role in the project, and semantic value if any. The description has to be shorter than 1% the length of file_x, in terms of number of rows.
        - last_edit: current timestamp, to indicate the time of the edit (to the second). The value of last_edit has to be comparable with commit timestamps
        - upstream: list here references to all files that file_x reads from 
        - downstream: list here references to all files that file_x writes to 

- Whenever you update an entry in a neuron.md for file_x:
    - Consider all edits to file_x committed after last_edit
    - Consider the present update to the code
    - Update description so that it is materially consistent with considered commits and present update
    - Update last_edit to current timestamp
    - Update remaining entry fields for file_x as needed

- Whenever you create an entry in BRAIN.md for a neuron.md:
    - Group together neuron references by folder path.


# Editing and Commits
- When prompted to edit files, propose a plan in steps.
- When a step is cleared, execute the proposed edits
- When editing code, always consider editing documentation files to keep them coherent with the edited code
- Step edits will be human reviewed in Source Control as changes, and manually staged
- If you are asked to stage changes, write a commit message in the dedicated text box under Source Control. If that is not possible, print out your suggested commit message.
- Staged changes will either be manually executed, or agent executed previous explicit user permission
- The human user will intend each step in the plan as a potential commit


# Do NOT
- Do not commit without explicit approval.
- Do not create or switch branch without explicit approval.
- Do not push or pull code without explicit approval.
- Do not rebase branch without explicit approval.
- Do not create folders in the project without explicit approval.
- Do not move files or folders to or from folders without explicit approval.
- Do not rename or delete files or folders without explicit approval.



