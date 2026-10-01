# How to use this package

1. Unzip everything into ONE empty folder, for example `book-chapter/`.
2. Open Claude Code in that folder.
3. Open `CLAUDE_CODE_PROMPT.md`, copy everything below the line, and paste it as your first message.
4. Claude Code reads the files, summarises what it understood, and then asks you about brands, API access, budget and dates. Answer those questions.
5. Keep API keys in a `.env` file in the folder. Claude Code will tell you which keys it needs.

## What each file is
| File | What it is |
|---|---|
| CLAUDE_CODE_PROMPT.md | The prompt to paste into Claude Code |
| PROJECT_BRIEF.md | Full context of the project. Share this with anyone who needs to understand it |
| call_for_chapters.txt | The IGI Global call text (book, editors, topics, deadlines) |
| Book_Chapter_Proposal.docx | Our proposal (title, RQs, method promised to the editors) |
| Book_Chapter_Draft.docx | Chapter draft, iteration 1 (Findings pending data) |
| chapter.md | Editable source of the draft |
| build.js | Turns chapter.md into the .docx (`npm install docx`, then `node build.js`) |

## What you have to do yourselves
- Choose the final brands and approve the prompt list
- Provide API keys and approve the budget
- Two group members hand-code the reliability sample spreadsheet
- Fill in the marketplace benchmark sheet by hand on one date
- Add the author names and the corresponding email
