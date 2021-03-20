import feedparser

from rest_framework import serializers

from rss_reader.users.models import User
from rss_reader.feeds.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    INVALID_URL_MESSAGE = 'This URL is invalid.'

    class Meta:
        model = Feed
        fields = '__all__'

    def validate_url(self, value):
        """
        Check that the feed's url is valid.
        """

        # This validation is only necessary when 
        # making POST requests (creating feeds)
        if self.context['request'].method != 'POST':
            return value

        user_id = int(self.initial_data.get('user'))
        user = User.objects.get(id=user_id)

        if Feed.does_feed_exist(user, value):
            raise serializers.ValidationError(
                'You already added this Feed.')

        if not Feed.is_url_valid(value):
            raise serializers.ValidationError(
                self.INVALID_URL_MESSAGE)
        return value

    def create(self, validated_data):
        """
        Override this method to get
        the posts of current feed
        after creating it
        """
        instance = super().create(validated_data)
        feed_data = instance.fetch_latest_posts()

        # Get original feed's name in case
        # user didn't put a custom name
        if not instance.name:
            instance.name = feed_data['feed']['title']
            instance.save()
        return instance
