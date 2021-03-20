from django.apps import AppConfig # noqa
from django.utils.translation import gettext_lazy as _ # noqa


class FeedsConfig(AppConfig):
    name = "rss_reader.feeds"
    verbose_name = _("Feeds")

    def ready(self):
        """
        This method is called ONLY ONCE
        when the server run for first time,
        so everytime we run the server locally
        or make deployment to production this
        file will execute the background task
        for updating feed's posts
        """
        from django.conf import settings

        from background_task.models import Task

        from rss_reader.feeds.tasks import update_feeds_posts

        # Only run the task if its not running
        try:
            Task.objects.get(
                verbose_name=settings.UPDATE_POSTS_TASK_VERBOSE_NAME)
        except Task.DoesNotExist:
            update_feeds_posts(
                repeat=settings.SECONDS_FOR_UPDATE_POSTS,
                verbose_name=settings.UPDATE_POSTS_TASK_VERBOSE_NAME)
        except Exception:
            """
            This error occurs when trying to run
            the background_task migrations
            the first time.

            This happens because the 'Task' model
            has not yet been created because the
            migrations have not run. So this should not
            happen after running migrations.
            """
            pass
