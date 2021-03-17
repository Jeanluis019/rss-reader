import asyncio

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for RSS Reader."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def update_feed_posts(self):
        """
        Update feeds asynchronously
        to keep posts up-to-date

        TODO:
        This can be improved by using
        a task that run in background
        and updates the feeds.
        """
        from rss_reader.feeds.models import Feed

        feeds_to_update = []
        for feed in self.feeds.all():
            if feed.does_can_update_posts():
                feeds_to_update.append({'id': feed.id, 'url': feed.url})

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(Feed.fetch_latest_posts(loop, feeds_to_update))
