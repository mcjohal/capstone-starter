# Part 1. Before you start

You need four free programs and two free accounts. If you already have something, skip that step. Allow about 30 minutes.

## Install the programs

1. **Python.** Go to [python.org/downloads](https://www.python.org/downloads/) and click the yellow Download button.
   * Windows: run the installer. On the first screen, **check the box "Add python.exe to PATH"**, then click Install Now.
   * Mac: run the installer and click through it.
2. **Git.** Go to [git-scm.com/downloads](https://git-scm.com/downloads), download the version for your computer, and install it. The default choice on every screen is fine.
3. **Visual Studio Code.** Go to [code.visualstudio.com](https://code.visualstudio.com/) and install it.
4. **The Python extension for VS Code.**
   1. Open VS Code.
   2. Click the Extensions icon on the left edge (four small squares), or press Ctrl + Shift + X.
   3. Search for **Python**.
   4. Install the one published by **Microsoft**.

## Check that they work

1. In VS Code, open a terminal: **Terminal** menu, then **New Terminal**. A panel opens at the bottom.
2. Type each line below and press Enter after each one. Each should print a version number.

   ```
   python --version
   git --version
   ```

   On a Mac, use `python3 --version`.

3. If Python says it is not recognized on Windows, the "Add to PATH" box was not checked. Run the Python installer again, choose **Modify**, and turn that option on. Then close VS Code completely and open it again.

## Tell Git who you are

Git labels every save with a name and email. In the same terminal, run these two lines with your own name and the email you will use for GitHub:

```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Make your accounts

1. **GitHub** (stores your code). Go to [github.com](https://github.com/) and click **Sign up**. Pick a professional username: employers may see it.
2. **Render** (runs your website). Go to [render.com](https://render.com/), click **Get Started**, and choose **GitHub** to sign up with the account you just made. One login then works for both.

Next: [Part 2. Get your copy](02-get-your-copy.md)
