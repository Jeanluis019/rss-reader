import feedparser # noqa

from rest_framework import serializers # noqa

from rss_reader.feeds.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'
