from django.apps import AppConfig # noqa
from django.utils.translation import gettext_lazy as _ # noqa


class FeedsConfig(AppConfig):
    name = "rss_reader.feeds"
    verbose_name = _("Feeds")
