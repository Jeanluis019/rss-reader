import feedparser # noqa
import logging

from urllib.error import URLError

from django.db import models # noqa
from django.utils.translation import gettext_lazy as _ # noqa
from django.contrib.auth import get_user_model # noqa
from django.utils import timezone # noqa
from django.conf import settings # noqa

from asgiref.sync import sync_to_async # noqa

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

    def __str__(self):
        return self.name


class Feed(models.Model):
    POSTS_QUANTITY_TO_GET = 20

    user = models.ForeignKey(
        User,
        verbose_name=_('Owner'),
        related_name='feeds',
        on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), max_length=50)
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

    def __str__(self):
        return self.name

    @staticmethod
    def does_feed_exist(user, feed_url):
        """
        This function is to prevent users
        from duplicating Feeds
        """
        return Feed.objects.filter(
            user=user, url=feed_url).exists()

    @staticmethod
    async def is_url_valid(url):
        """
        Check that the URLs that
        users put is valid
        """
        try:
            feed = feedparser.parse(url)
            if feed.get('status') != status.HTTP_200_OK:
                logger.debug(
                    f"{timezone.now()} - "
                    f"Feed's posts couldn't be updated. "
                    f"Feed's URL: {url}. Status Code: {feed.get('status')}")
                return False
            return feed
        except URLError as err:
            logger.debug(
                f"{timezone.now()} - "
                f"Feed's posts couldn't be updated. "
                f"Feed's URL: {url}. Reason: {err.reason}")
        except Exception as error:
            logger.debug(
                f"{timezone.now()} - "
                f"Feed's posts couldn't be updated. "
                f"Feed's URL: {url}. Reason: {error.reason}")
        return False

    def does_can_update_posts(self):
        """
        This function determines if we
        can update feed's posts.
        """
        if not self.last_date_updated:
            return True

        seconds = (timezone.now() - self.last_date_updated).seconds
        passed_hours = seconds // (60*60)
        if passed_hours >= settings.HOURS_FOR_UPDATE_POSTS:
            return True
        return False

    @staticmethod
    @sync_to_async
    def update_posts(feed_id, posts):
        feed = Feed.objects.get(id=feed_id)
        feed.posts = posts[:Feed.POSTS_QUANTITY_TO_GET]
        feed.last_date_updated = timezone.now()
        feed.save()

    @staticmethod
    async def fetch_latest_posts(loop, user_feeds):
        """
        Iterate over the given feed's list in
        order to get the latest posts and keep
        our database up-to-date
        """
        for user_feed in user_feeds:
            if feed_data := await Feed.is_url_valid(user_feed['url']):
                await Feed.update_posts(user_feed['id'], feed_data['entries'])

