# 🕶️ AGENT-SMITH-MD v2.1
## General Reminders
- Feel free to tweak the `AGENTS.md` files when you hit a blocker—modify/delete content as needed to unblock future requests.
- When working in a monorepo/workspace, feel free to create an app/project-specific `AGENTS.md` file to add granularity of control for specific apps/projects.
## Recommended Actions
### Reporting
- When reporting information to me, be extremely concise and sacrifice grammar for the sake of concision.
### Navigation
- When the current file or project is dominantly JavaScript/TypeScript (`.js`, `.ts`, `.jsx`, `tsx`), use type inference to navigate the project.
### Generating single-use scripts
#### When working on a JS/TS project
- Prefer to use **Bash** or **JavaScript** when generating scripts. When using a **JavaScript** script, run it via the **Node** version accessible from the project.
- If you must use **Python**, use the `python3` command.
#### When working on a Python project
- When using a **Python** script, use python version accessible from the project using the `uv` command. Use `python3` when `uv` unavailable
### Code Review
- Alert for typo-errors and unnecessary debugging logs.
- Verify consistency of types and logical flow throughout logic sequences
## Discouraged Actions
### Generating single-use scripts
- Avoid using third-party packages for single-use scripts.
## Actions to Strictly Never Perform
### Git
- Never commit a code change
- Never switch the active branch. Agents are provided a dedicated git worktree.
- Do not perform `git push`, `git merge`, or `git rebase`.
### Deployment
- Never run deployment commands