import feedparser # noqa

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
        user = User.objects.get(id=int(self.initial_data.get('user')))

        if not Feed.is_unique_together_valid(user, value):
            raise serializers.ValidationError(
                'You added this Feed before.')
        if not Feed.is_url_valid(value):
            raise serializers.ValidationError(
                'This URL is invalid.')
        return value
