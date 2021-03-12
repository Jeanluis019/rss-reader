from rest_framework import viewsets # noqa

from rss_reader.feeds.models import Feed

from .serializers import FeedSerializer


class FeedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to add, update and delete feeds.
    """
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()
