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
- Whenever you receive a prompt, use the agent_neuron.md file references in AGENTS.md and their tags to help you inform your plan about which repo resources are pertinent to your task.
- Whenever you access a folder as part of a task, if the folder contains a agent_neuron.md, include agent_neuron.md in your current session context
- Whenever plan to inspect files in folder X, check first whether a agent_neuron.md file is present in X:
    - If no such file is present:
        - create it and name it after X's path
        - inspect the files of interest in X and add an entry in agent_neuron.md for each file in X where you sum up the file content, its pertinence to your present task, and related metadata pertinent to your ability to analyze it (like file size),  for future reference. The file entry in agent_neuron.md has to be small compared to the file's content.
        - Consider X parent folder, Y:
            - If Y is not the root, and there is a agent_neuron.md in Y, update it whith a reference to the newly created X/agent_neuron.md
            - If Y is the project root, add a reference to the newly created agent_neuron.md to AGENTS.md, 
            - If you add a reference to a agent_neuron.md file in a .md file, tag the reference to help codex determine its relevance to future user prompts.
    - If a agent_neuron.md file is present for X, re-evaluate which files to inspect in X based on your current task, and on the descriptions and task relevance you find in agent_neuron.md about said files

# Editing and Commits
- When prompted to edit files, propose a plan in steps. Each step is ideally a commit
- When editing code, always consider editing .md files, context files, documentation files, readme files to keep the coherent with the edited code.
- Don't commit without explicit approval.
- Whenever a task requires you to inspect folders and files, consider the <context>.md file closest to the object of your inspection: update the <context>.md file with a concise sum-up of your inspection findings for future reference. Keep the list of context references updated in the AGENT.md file (present file). As the development proceeds, this practice will create a content map of the project that should help you save processing time on file and folder inspection.