from rest_framework import viewsets # noqa
from rest_framework import status # noqa
from rest_framework.decorators import action # noqa
from rest_framework.response import Response # noqa

from rss_reader.feeds.models import Feed

from .serializers import FeedSerializer


class FeedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users
    to get, add, update and delete Feeds.
    """
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user.id)
