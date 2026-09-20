# Elaboration
- Evaluate the complexity of your task:
    - Consider asking the user to switch to higher effort
    - Consider asking approval to spawn a more advanced models

# Coding Style
- Include code features that were not explicitly asked for only if you deem them strictly necessary
- Try to keep the code human understandable
- Divide the code into section, and add concise 1 line comments in the code to explain the function of each code section. Avoid comment redundancy.
- Add concise 1 line comments in the code to explain the working of code subsections when you deem it not obvious by words used in the code or too complex.
- DNY: do not repeat yourself. If two chuncks of code in a file define very similar processing logic, modularize the logic into a single function.

# Editing and Commits
- When prompted to edit files, propose a plan in steps. Each step is ideally a comment
- When editing code, always consider editing .md files, context files, documentation files, readme files to keep the coherent with the edited code.
- Whenever a task requires you to inspect folders and files, consider the <context>.md file closest to the object of your inspection: update the <context>.md file with a concise sum-up of your inspection findings for future referemce. Keep the list of context references updated in the AGENT.md file (present file). As the development proceeds, this practice will create a content map of the project that should help you save procssing time on file and folder inspection.
- When editing files, show diff and ask for approval.
- Don't commit without explicit approval.