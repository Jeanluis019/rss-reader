import feedparser # noqa

from django.test.testcases import SerializeMixin # noqa

from rest_framework import status # noqa
from rest_framework.test import APITestCase # noqa

from rss_reader.users.models import User
from rss_reader.feeds.models import Feed, FeedCategory


class FeedTestCaseMixin(SerializeMixin):
    """
    Mixin for testing the create, update,
    and delete methods of Feeds API
    """

    lockfile = __file__

    def setUp(self):
        self.user = User.objects.create_user(**{
            'username': 'jonh',
            'password': 'my_secret_password',
            'email': 'john@test.com'
        })
        self.feed_mockup = {
            'user': self.user.id,
            'name': 'Lifehack',
            'category': FeedCategory.objects.create(
                user=self.user, name='Productivity').id,
            'url': 'https://www.lifehack.org/feed'
        } 
        self.created_feed_id = None
        self.client.force_authenticate(self.user)
        self.feed = self.client.post('/api/feeds/', self.feed_mockup)


class CreateFeedTest(FeedTestCaseMixin, APITestCase):
    """
    Test API for inserting a new Feed
    """
    def test_create(self):
        feed_data = self.feed.json()

        self.assertEqual(self.feed.status_code, status.HTTP_201_CREATED)
        self.assertEqual(feed_data['user'], self.feed_mockup['user'])
        self.assertEqual(feed_data['name'], self.feed_mockup['name'])
        self.assertEqual(feed_data['category'], self.feed_mockup['category'])
        self.assertEqual(feed_data['url'], self.feed_mockup['url'])

        # Test that we got the posts of current feed
        self.assertIsInstance(feed_data['posts'], list)
        self.assertGreater(len(feed_data['posts']), 0)


class UpdateFeedTest(FeedTestCaseMixin, APITestCase):
    """
    Test API for updating an existing Feed
    """
    def test_update(self):
        feed_data = self.feed.json()
        new_data = {
            'name': 'Los Angeles Times',
            'category': FeedCategory.objects.create(
                user=self.user, name='News').id,
            'url': 'https://www.latimes.com/local/rss2.0.xml'
        }

        response = self.client.patch(f"/api/feeds/{feed_data['id']}/",new_data)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['user'], self.feed_mockup['user'])
        self.assertEqual(response_data['name'], new_data['name'])
        self.assertEqual(response_data['category'], new_data['category'])
        self.assertEqual(response_data['url'], new_data['url'])


class DeleteFeedTest(FeedTestCaseMixin, APITestCase):
    """
    Test API for deleting a Feed
    """
    def test_delete(self):
        feed_data = self.feed.json()
        self.client.delete(f"/api/feeds/{feed_data.get('id')}/")
        self.assertFalse(
            Feed.objects.filter(id=feed_data.get('id')).exists())


# TODO: Create a test for validate unique_together fields are working
# TODO: Save the Feeds URL API in a variable
