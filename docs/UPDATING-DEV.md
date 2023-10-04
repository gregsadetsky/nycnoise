### how do you update dev and keep up to date?

generally speaking, you:
- `git pull` while in the dev branch
- then `pip install -r requirements.txt` to get the latest requirements and finally
- `python manage.py migrate`

none of these commands (the `git pull`, the `pip install` or the `migrate`) will do anything bad or hurt. they can be run at any time.

but you should almost definitely always run `pip install` and `migrate` after fetching new code on a branch!
