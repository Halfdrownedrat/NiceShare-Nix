from i18n_modern import I18nModern

from niceshare.helper.config import settings
from niceshare.helper.paths import get_path

""" Module for internationalization (translation)"""
i18n = I18nModern(settings.language, str(get_path(f"{settings.language}.yml", "locales")))
