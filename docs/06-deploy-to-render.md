# Part 6. Deploy to Render

Render copies your project from GitHub, installs Flask, and runs your app on the internet at an address like `https://recipe-box.onrender.com`. The free tier is enough for this project. Allow about 15 minutes the first time.

**Before you start:** your app works on your computer, `python check.py` passes, `config.py` says `"my_project"`, and your latest work is pushed to GitHub (Part 5). Render runs whatever is on GitHub, not what is on your computer.

## Create the web service

1. Go to [dashboard.render.com](https://dashboard.render.com/) and sign in with GitHub.
2. Click **New**, then **Web Service**.
3. Under **Source Code**, choose **GitHub** and find your repository in the list.
   * If it is not listed, click **Configure GitHub** (or **Configure account**), choose your GitHub account, give Render access to that repository (or all repositories), click **Save**, and return to Render.
4. Click your repository. A settings form opens. Fill it in like this:

   | Setting | Value |
   |---|---|
   | Name | Your site's name, like `recipe-box`. It becomes your web address. |
   | Language | **Python 3** |
   | Branch | **main** |
   | Region | The one closest to you |
   | Root Directory | Leave it empty |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `gunicorn app:app` |
   | Instance Type | **Free** |

   Render changes the labels on this form from time to time. If one doesn't match exactly, pick the closest one.

5. Click **Deploy Web Service** at the bottom.

## Watch it build

1. Render shows a log while it works. It installs Flask and gunicorn, then starts your app. This takes 2 to 5 minutes.
2. When the log says **Your service is live**, click the address at the top of the page (it ends in `.onrender.com`).
3. Click through every page to check them.
4. Copy the address. You need it for your README and your Capstone page.

## Updates are automatic

Every time you push to GitHub (Part 5), Render notices and deploys the new version within a few minutes. Watch the **Events** tab to see it happen.

## What to expect on the free tier

* **It goes to sleep.** After about 15 minutes with no visitors, Render pauses your app. The next visitor waits up to a minute while it wakes up. That is normal, not a bug.
* **It forgets added rows.** Each time it wakes or redeploys, the app rebuilds the database from your SQL files. Anything added on the Add page disappears. Your seed.sql data is always there.
* **No credit card needed.** If Render asks for payment, check that **Free** is selected as the Instance Type.

## If the deploy fails

1. Open the **Logs** tab and scroll to the first red error.
2. Common causes:
   * **`No module named ...`**: requirements.txt is missing or was changed. It should hold the two lines `Flask` and `gunicorn` with their version numbers, as in the starter.
   * **`Failed to find attribute 'app'`**: the Start Command has a typo. It must be exactly `gunicorn app:app`.
   * **The site works but every page says it is waiting for its SQL**: `config.py` still says `"library_example"`, or your SQL files were not pushed. Fix it, then commit and push.
   * **The site works but shows the library**: same cause. `config.py` on GitHub must say `"my_project"`.
3. After a fix, commit and push. Render deploys again by itself. You can also click **Manual Deploy**, then **Deploy latest commit**.

Next: [Part 7. Add it to your Capstone page](07-add-to-capstone-page.md)
