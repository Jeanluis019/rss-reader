import feedparser # noqa

# from django.test.testcases import SerializeMixin # noqa

from rest_framework import status # noqa
from rest_framework.test import APITestCase # noqa

from rss_reader.users.models import User
from rss_reader.feeds.models import Feed, FeedCategory


class FeedTestCase(APITestCase):
    """
    Mixin for testing the create, update,
    and delete methods of Feeds API
    """
    BASE_API_URL = '/api/feeds/'

    lockfile = __file__

    def setUp(self):
        self.user = User.objects.create_user(**{
            'username': 'jonh',
            'password': 'my_secret_password',
            'email': 'john@test.com'
        })
        self.feed_mockup = {
            'user': self.user.id,
            'category': FeedCategory.objects.create(
                user=self.user, name='Productivity').id,
            'url': 'https://www.lifehack.org/feed'
        }
        self.client.force_authenticate(self.user)
        self.feed = self.client.post(self.BASE_API_URL, self.feed_mockup)
        self.feed_data = self.feed.json()

    def test_create(self):
        """
        Test API for inserting a new Feed
        """
        original_feed_name = 'Lifehack'

        self.assertEqual(self.feed.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.feed_data['user'], self.feed_mockup['user'])
        self.assertEqual(self.feed_data['name'], original_feed_name)
        self.assertEqual(self.feed_data['category'], self.feed_mockup['category'])
        self.assertEqual(self.feed_data['url'], self.feed_mockup['url'])

        # Make sure we got the Feed's posts
        self.assertIsInstance(self.feed_data['posts'], list)
        self.assertGreater(len(self.feed_data['posts']), 0)

    def test_fetching_feeds(self):
        response = self.client.get(self.BASE_API_URL)
        user_feeds_count = self.user.feeds.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), user_feeds_count)

    def test_can_get_a_single_feed(self):
        response = self.client.get(f"{self.BASE_API_URL}{self.feed_data['id']}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        """
        Test API for updating an existing Feed
        """
        
        new_data = {
            'name': 'Los Angeles Times',
            'category': FeedCategory.objects.create(
                user=self.user, name='News').id,
            'url': 'https://www.latimes.com/local/rss2.0.xml'
        }

        response = self.client.patch(f"{self.BASE_API_URL}{self.feed_data['id']}/",new_data)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['user'], self.feed_mockup['user'])
        self.assertEqual(response_data['name'], new_data['name'])
        self.assertEqual(response_data['category'], new_data['category'])
        self.assertEqual(response_data['url'], new_data['url'])

    def test_delete(self):
        """
        Test API for deleting a Feed
        """
        self.client.delete(f"{self.BASE_API_URL}{self.feed_data.get('id')}/")
        self.assertFalse(
            Feed.objects.filter(id=self.feed_data.get('id')).exists())

    def test_do_not_duplicate_feeds(self):
        """
        Make sure the method 'does_feed_exist'
        is working properly, so we can avoid
        that users can duplicate feeds
        """
        response = self.client.post(self.BASE_API_URL, self.feed_mockup)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('url')[0], 'You already added this Feed.')

    def test_feed_with_custom_name(self):
        """
        If we don't pass a name in the request,
        the app save the original feed's name,
        so we must to make sure that when
        we pass a custom name, the app save it
        instead of the original.
        """
        mockup = {
            'user': self.user.id,
            'name': 'A Custom Name',
            'category': FeedCategory.objects.create(
                user=self.user, name='Productivity').id,
            'url': 'https://www.politico.com/rss/politicopicks.xml'
        }
        response = self.client.post(self.BASE_API_URL, mockup)
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json['user'], mockup['user'])
        self.assertEqual(response_json['name'], mockup['name'])
        self.assertEqual(response_json['category'], mockup['category'])
        self.assertEqual(response_json['url'], mockup['url'])

        # Make sure we got the Feed's posts
        self.assertIsInstance(response_json['posts'], list)
        self.assertGreater(len(response_json['posts']), 0)    

# TODO: Test the background task for updating feed's posts
# TODO: Test creating feed with bad url
# TODO: Test IndexView
# TODO: Test LogoutView