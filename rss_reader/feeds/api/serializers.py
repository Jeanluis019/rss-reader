import feedparser # noqa

from asgiref.sync import async_to_sync # noqa

from rest_framework import serializers # noqa
from rest_framework.validators import UniqueTogetherValidator # noqa

from rss_reader.users.models import User
from rss_reader.feeds.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'

    def validate_url(self, value):
        """
        Check that the feed's url is valid.
        """
        user_id = int(self.initial_data.get('user'))
        user = User.objects.get(id=user_id)

        if Feed.does_feed_exist(user, value):
            raise serializers.ValidationError(
                'You added this Feed before.')

        is_url_valid_sync = async_to_sync(Feed.is_url_valid)
        if not is_url_valid_sync(value):
            raise serializers.ValidationError(
                'This URL is invalid.')
        return value
