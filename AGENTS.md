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

# Project Brain
Expect a BRAIN.md in the project root.

- Whenever you receive a prompt, consult BRAIN.md. for file references and related taggs. Use the referenced files that you deem more relevant to your task, to inform your plan for addressing the task. 

- Whenever you access a folder as part of a task, if the folder contains a neuron.md, include neuron.md in your current session context.

- Whenever you edit code (like SQL or Python) in a file file_x, in folder folder_x, check whether a neuron.md file is present in folder_x. Then:
    - If no neuron.md file is present:
        - create a neuron.md in folder_x
        - write in neuron.md a reference to its closest neuron.md ancestor. If there is no ancestor, reference BRAIN.md as closest ancestor
        - Add to the closest ancestor or BRAIN.md a reference to neuron.md
        - write in neuron.md a reference to its closest neuron.md descendants, if any.
        - For each referenced descendant in neuron.md, update the descendant reference to the closest ancestor.
        - create an entry in neuron.md for file_x
        - Create an entry BRAIN.md 
    - If a neuron.md file is present in folder_x: 
        - Create or update the entry for file_x in neuron.md
        - Update the closest ancestor reference in the neuron

- Whenever you create an entry in a neuron.md for file_x:
    - add in neuron.md a reference to file_x
    - write a summary description of file_x functionalities
    - add the id and date of the last known commit to file_x
    - If in the course of the present task you have noticed upstream or downstream dependencies of file_x, add them in the entry as references.

- Whenever you update an entry in a neuron.md for file_x:
    - Edit the entry so that it is materially consistent with the edited code
    - Check the date of the last known commit to file_x: if there is a more recent commit to file_x: 
        - Based on the last commit edits, check the material consistency of the file_x entry with file_x, and update the entry accordingly
        - Update the date and id of last known commit to the most recent commit

- Whenever you create an entry in BRAIN.md for a neuron.md:
    - add a reference to neouron.md
    - add a list of tags that would help you determine the neuron's relevance to future tasks
    - Group together neuron entries at the same folder level.


# Editing and Commits
- When prompted to edit files, propose a plan in steps. Each step is ideally a commit
- When editing code, always consider editing .md files, context files, documentation files, readme files to keep them coherent with the edited code:
    - Files that describe working logic should be updated when implemented logic changes
    - Files that describe file contents should change when file contents change
    - Files that describe workflow events have to be updated when the user takes project decisions like: stated project objectives, methods, technologies of choice...
- Don't commit without explicit approval.
- Whenever a task requires you to inspect folders and files, consider the <context>.md file closest to the object of your inspection: update the <context>.md file with a concise sum-up of your inspection findings for future reference. Keep the list of context references updated in the AGENT.md file (present file). As the development proceeds, this practice will create a content map of the project that should help you save processing time on file and folder inspection.
