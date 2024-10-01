import os
from pathlib import Path

import dj_database_url
from django.utils.log import DEFAULT_LOGGING
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# setting to False by default
DEBUG = False

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")


# Application definition

INSTALLED_APPS = [
    "dal",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "core",
    # https://github.com/jazzband/django-tinymce/
    "tinymce",
    # https://github.com/jrief/django-sass-processor
    "sass_processor",
    # https://github.com/lazybird/django-solo
    "solo",
    # https://github.com/django-ordered-model/django-ordered-model
    "ordered_model",
    # https://github.com/nephila/django-meta
    "meta",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

ROOT_URLCONF = "nycnoise.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.parent / "core/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- TinyMCE configurations --- #
# More information: https://www.tiny.cloud/docs/general-configuration-guide/ #

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}
TINYMCE_SPELLCHECKER = True


WSGI_APPLICATION = "nycnoise.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

USE_I18N = True

USE_TZ = True
# from the docs:
# When USE_TZ is True, [TIME_ZONE] is the default time zone that Django will use to display
# datetimes in templates and to interpret datetimes entered in forms
TIME_ZONE = "America/New_York"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

CORE_FOLDER = BASE_DIR.parent
WHITENOISE_ROOT = BASE_DIR / "staticroot"
SASS_PROCESSOR_ROOT = CORE_FOLDER / "core/static/"
STATICFILES_DIRS = [CORE_FOLDER / "core/static/core"]

# https://stackoverflow.com/a/76117900
# overridden in test.py
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # https://whitenoise.readthedocs.io/en/latest/index.html
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

# start from default values -- so that they can be overriden later
# https://stackoverflow.com/a/25508761
LOGGING = DEFAULT_LOGGING

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

RC_DEVELOPER_INTERNAL_TOKEN = os.environ["RC_DEVELOPER_INTERNAL_TOKEN"]
PROD_INTERNAL_API_SERVER = os.environ["PROD_INTERNAL_API_SERVER"]

SITE_ID = 1


# https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-django
def custom_show_pyinstrument(request):
    return request.user.is_superuser


PYINSTRUMENT_SHOW_CALLBACK = "nycnoise.settings.base.custom_show_pyinstrument"
PYINSTRUMENT_ENABLE = os.environ["PYINSTRUMENT_ENABLE"] == "true"
if PYINSTRUMENT_ENABLE:
    MIDDLEWARE += [
        "pyinstrument.middleware.ProfilerMiddleware",
    ]

# Django-meta configuration
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_TITLE_TAG = True
META_SITE_PROTOCOL = "https"
META_SITE_DOMAIN = "nyc-noise.com"
META_SITE_TYPE = "website"
META_TWITTER_TYPE = "summary_large_image"
