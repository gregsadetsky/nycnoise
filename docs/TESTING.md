### how to test

```bash
source venv/bin/activate
python manage.py test
```

- tests must be run with a postgresql database -- sqlite won't work, as we use some postgresql-specific indices (for full text search) that would be hard to rip out from the codebase. those indices are fully incompatible with sqlite.
