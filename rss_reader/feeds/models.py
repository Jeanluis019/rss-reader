import feedparser # noqa
import logging

from urllib.error import URLError

from django.db import models # noqa
from django.utils.translation import gettext_lazy as _ # noqa
from django.contrib.auth import get_user_model # noqa
from django.utils import timezone # noqa
from django.conf import settings # noqa

from rest_framework import status # noqa

logger = logging.getLogger(__name__)

User = get_user_model()


class FeedCategory(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('Owner'),
        related_name='feed_categories',
        on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), max_length=50)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Feed(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('Owner'),
        related_name='feeds',
        on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=50,
        blank=True,
        null=True)
    category = models.ForeignKey(
        FeedCategory,
        verbose_name=_('Category'), 
        blank=True,
        null=True,
        related_name='feeds', 
        on_delete=models.SET_NULL)
    url = models.URLField(verbose_name=_('URL'), max_length=200)
    posts = models.JSONField(_("Posts"), blank=True, null=True)
    last_date_updated = models.DateTimeField(
        _("Last update"), blank=True, null=True)


    class Meta:
        ordering = ('-id',)
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')
        unique_together = ['user', 'url']

    @staticmethod
    def does_feed_exist(user, feed_url):
        """
        This function is to prevent users
        from duplicating Feeds
        """
        return Feed.objects.filter(
            user=user, url=feed_url).exists()

    @staticmethod
    def is_url_valid(url):
        """
        Check that Feed's URL is valid and
        log any errors if there are any.
        """
        debug_message = (
            f"{timezone.now()} - "
            f"Feed's posts couldn't be updated. Feed's URL: {url}. "
            "Reason: {error}")

        try:
            feed = feedparser.parse(url)
            if feed.get('status') == status.HTTP_200_OK:
                return feed

            logger.debug(debug_message.replace(
                "Reason: {error}", f"Status Code: {feed.get('status')}"))
        except (URLError, Exception) as error:
            logger.debug(debug_message.format(error=error.reason))

        return False

    def fetch_latest_posts(self):
        """
        Call the Feed's URL in order to
        get the latest posts and keep
        our database up-to-date
        """
        if feed_data := Feed.is_url_valid(self.url):
            posts = feed_data['entries']
            self.posts = posts[:settings.POSTS_QUANTITY_TO_GET]
            self.last_date_updated = timezone.now()
            self.save()

            return feed_data
