#!/usr/bin/env bash
# exit on error
set -o errexit

gunicorn --log-level debug -b 0.0.0.0:8000 --access-logformat '%(h)s %(l)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" reqtime: %(M)s ms' nycnoise.wsgi:application
