# py26-u07 – Tone Printer

**u07** · Python course 2026/27 · week 6

Each project lives in its own directory, together with the brief, my notes and
the self-check script. The brief is the source of truth; this file only
explains the workflow.

## Week 6 – Tone Printer

- directory: `tone_printer/`
- brief: `tone_printer/PROJEKT.md` (the same text is in `tone_printer/PROJEKT.pdf`)

## Workflow

1. Fork this repository to your own account (once per repository).
2. Clone your fork and add this repository as `upstream`.
3. Create a branch for the week, for example `w06-tone_printer`.
4. Work inside `tone_printer/` only.
5. Run the check before you push:

   ```bash
   cd tone_printer
   python3 check.py
   ```

6. Commit, push to your fork and open a pull request against `main` here.
7. Answer the review comments in the same pull request.

The first commands, once:

```bash
git clone git@github.com:<your-login>/py26-u07.git
cd py26-u07
git remote add upstream git@github.com:CKZiU-Codelab/py26-u07.git
```

## Rules

- Work only inside `tone_printer/`.
- Keep the files your program produced: the CSV, the images and the reports.
  They are the result, not a side effect.
- Do not edit `check.py`; it is the teacher's file.
- No secrets and no files from outside the project directory.
