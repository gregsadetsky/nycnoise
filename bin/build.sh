#!/usr/bin/env bash
# exit on error
set -o errexit

# used to be necessary on render -- not anymore?
# pip install --upgrade pippip install --force-reinstall -U setuptools
pip install -r requirements.txt

# run tests -- build should fail if they fail!
DJANGO_SETTINGS_MODULE=nycnoise.settings.test python manage.py test --noinput

# all good, proceed!
python manage.py compilescss
python manage.py collectstatic --no-input
python manage.py migrate
