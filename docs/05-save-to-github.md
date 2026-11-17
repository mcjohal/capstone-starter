# Part 5. Save to GitHub

Your project already lives on GitHub (you copied it there in Part 2), but the changes you make in VS Code stay on your computer until you **commit** and **push** them.

* A **commit** is a saved snapshot of your work, with a short message saying what changed.
* A **push** sends your commits up to GitHub.

Do this every time you finish a step, so your work is backed up and your instructor can see your progress.

## Commit and push in VS Code

1. Save all your files: **File**, then **Save All**.
2. Click the **Source Control** icon on the left edge (Ctrl + Shift + G). A number on the icon shows how many files changed.
3. Look at the list under **Changes**. Click a file to see exactly what changed, in red (removed) and green (added).
4. In the **Message** box at the top, type what you did, such as `Add tables and sample rows`.
5. Click **Commit**. If VS Code asks whether to stage all your changes and commit them directly, click **Yes** (or **Always**).
6. Click **Sync Changes** (the same button, now showing an up arrow and a number). If VS Code asks to confirm, click **OK**.
7. The first time, VS Code may ask you to sign in to GitHub. Click **Allow** and sign in in the browser.

## Check that it worked

1. Open your repository on github.com.
2. Refresh the page. Your commit message appears next to the files you changed, and the files show your new SQL.

## What does not go to GitHub

The `.gitignore` file keeps two things out on purpose, so do not worry when you don't see them on GitHub:

* `.venv`, your Python environment. Render builds its own.
* `instance`, the database file. It is rebuilt from your SQL files every time the app starts.

## If something goes wrong

* **"Please tell me who you are"**: you skipped Tell Git who you are in Part 1. Run those two `git config` lines in the terminal, then commit again.
* **Sync fails because GitHub has changes you don't have** (for example, you edited the README on the GitHub website): click the **...** menu at the top of Source Control, choose **Pull**, then Sync again.

Next: [Part 6. Deploy to Render](06-deploy-to-render.md)
