import feedparser # noqa

from django.db import models # noqa
from django.utils.translation import gettext_lazy as _ # noqa
from django.contrib.auth import get_user_model # noqa

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
    user = models.ForeignKey(
        User,
        verbose_name=_('Owner'),
        related_name='feeds',
        on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    category = models.ForeignKey(
        FeedCategory,
        verbose_name=_('Category'), 
        blank=True, null=True,
        related_name='feeds', 
        on_delete=models.SET_NULL)
    url = models.URLField(verbose_name=_('URL'), max_length=200)
    posts = models.JSONField(_("Posts"), blank=True, null=True)


    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')

    def __str__(self):
        return self.name

    def fetch_latest_posts(self):
        """
        Get the latest posts from the current feed
        to keep our database up-to-date
        """
        feed = feedparser.parse(self.url)

        # Just get the latest 20 posts
        self.posts = feed['entries'][:20]
        self.save()

    def save(self, *args, **kwargs):
        """
        Override Django's save method
        to make custom modifications
        """
        super().save(*args, **kwargs)

        if self.url and not self.posts:
            self.fetch_latest_posts()
