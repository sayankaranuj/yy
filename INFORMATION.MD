1.FIRST SEE ALL THE FOLDERS OF SEPRATE PROJECT LIKE AUTHZ0, BCHACKTOOL,CLAUDBUGBOUNTY, HACKINGTOOL, SESSION HIJACKING, WEBSCRAPPING UNDERSTAND ALL THIS FOLDER FIRST
2. AFTER THAT UNDERSTAND IN DETAILD THE INSTRUCTION.MD AND START WORKING ON ONE BY ONE PROMT AS PER THE INSTRUCTION 

3. DONT ASK ME EACH TIME FOR CONFIRMATION SEE YOURSELF AND START NEXT WORK


4. EACH TIME UPATE THE IFNORAMTION WHAT YOU HAVE DONE TILL NOW IN SINGLE README.MD FILE IN SIMPLE EXPLANATION NOT TOO LONG JUST FOR UNDERSTANDING THE ANOTHER COPILOT

5. READ README.MD FILE OF AGENTSEC-AI EACH TIME TO SEE WHERE THE TASK IS COMPLETE AND HOW MUCH DONE TILL NOW

6. EACH TIME ALSO ADD THE OUT PAST CONVERSATION IN README.MD INSIDE AGENTSEC-AI FOR UNDERSTANDING OTHER COPILOT

7. dont ask me again and again for confirmation or anything to do next task just do your work continuously and  this is final warning just do your work continuously


Next action (in progress): run and fix tests/test_api_routes.py::test_celery_scan_task_is_registered (verifying Celery task registration), then continue with the remaining failing tests in order. I'll proceed and report back with the result of each test/fix.



GOLDEN RULES — FOLLOW ALWAYS:
1. Never verify or test mid-phase. Only verify at end of each phase.
2. Never regenerate existing code. Ask before overwriting anything.
3. Never hardcode secrets. Always use .env + python-dotenv.
4. Never use print(). Use Python logging module only.
5. Always write async functions where FastAPI or SQLAlchemy supports it.
6. Always write docstrings on every function and class.
7. Generate files in dependency order always.
8. When I say "generate X", generate only X. Do not generate Y and Z 
   unless I ask.
9. Batch related small files in one response to save tokens.
10. Do not explain what you are going to do. Just do it.
11. Do not add placeholder comments like "# add logic here". 
    Write actual working logic.
12. Use absolute imports everywhere. No relative imports.
13. Every Celery task must have: bind=True, max_retries=3, 
    autoretry_for=(Exception,)
14. All database operations must use async sessions.
15. Do not proceed to next phase unless I explicitly say so.


# Copilot Instructions — Token Efficiency

## Output rules (highest impact — output costs more than input)
- Code only. No explanations, no summaries, no "Here's what I did" preambles, unless I explicitly ask "explain" or "why".
- No restating my question back to me.
- No repeating unchanged code — only show the diff/changed lines, not the whole file, unless I ask for the full file.
- Bullets over paragraphs. One-line answers where possible.
- Skip disclaimers, caveats, and "note that" asides unless they change correctness.

## Context rules
- Don't re-read files you've already seen in this session unless they changed.
- Don't explore the whole repo for small, scoped tasks — use only the files I reference or that are directly imported by them.
- Ask before running broad searches (e.g. grep across entire repo) if a targeted file lookup would do.

## Behavior rules
- Be precise, not exploratory. Assume I know what I'm asking for; don't hedge with multiple alternative approaches unless I ask for options.
- If a fix is one line, give one line — don't refactor surrounding code unless asked.
- No emojis, no markdown headers in chat responses unless the answer is genuinely long-form documentation.