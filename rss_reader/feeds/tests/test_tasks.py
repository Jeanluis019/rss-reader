from django.test import TestCase

from rss_reader.users.models import User

from rss_reader.feeds.models import Feed, FeedCategory
from rss_reader.feeds.tasks import update_feeds_posts


class UpdateFeedsPostsTest(TestCase):

    def setUp(self):
        """
        Create a feed without posts
        to update the posts with the
        background tasks later
        """
        user = User.objects.create(username='testuser')
        self.feed = Feed.objects.create(**{
            'user': user,
            'name': 'Test Feed',
            'category': FeedCategory.objects.create(
                user=user, name='Productivity'),
            'url': 'https://www.lifehack.org/feed'
        })

    def test_feed_without_posts(self):
        """
        Make sure the feed created previously
        doesn't has posts yet
        """
        self.assertEqual(self.feed.posts, None)

    def test_update_posts_task(self):
        """
        Make sure the feed created previously
        has some posts after running the task
        """
        # Run the tasks immediately
        update_feeds_posts.now()

        # Get the feed instance with the 'posts' field updated
        self.feed = Feed.objects.get(id=self.feed.id)

        self.assertIsInstance(self.feed.posts, list)
        self.assertGreater(len(self.feed.posts), 0)
