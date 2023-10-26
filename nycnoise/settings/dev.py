from .base import *

# debug is set to false by default just in case
DEBUG = True

# reallllly amazing trick to SHOW undefined/invalid strings in the templates
# instead of not displaying them (which is super duper confusing)
# i.e. {{ event.wrongkey }} would normally not show up at all in the templates if `wrongkey` did not
# exist or was a typo... with the trick below, it will show up! amazing.
# https://stackoverflow.com/questions/4300442/show-undefined-variable-errors-in-django-templates#comment131874878_4300506
TEMPLATES[0]["OPTIONS"]["string_if_invalid"] = "MISSING! {{ %s }}"
