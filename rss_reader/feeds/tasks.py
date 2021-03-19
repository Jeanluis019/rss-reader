"""
In this file we going to create
classes and methods that require
run tasks in background asynchronously
"""
from logging import getLogger

from django.conf import settings # noqa

from background_task import background

from .models import Feed

logger = getLogger(__name__)

# Execute this task
# 20 seconds after call it
@background(schedule=20)
def update_feeds_posts():
    """
    Iterate over all Feeds in order to
    update their posts and make sure
    users have the latest news from
    their Feeds
    """
    logger.debug("Background Task 'update_feeds_posts' started")

    for feed in Feed.objects.all():
        try:
            feed.fetch_latest_posts()
        except Exception as error:
            logger.debug(
                'Fail to update posts. '
                f'Feed ID: {feed.id} ',
                f'Error: {error}')

    logger.debug("Background Task 'update_feeds_posts' finished")
