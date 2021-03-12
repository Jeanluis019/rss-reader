from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from rss_reader.users.api.views import UserViewSet
from rss_reader.feeds.api.views import FeedViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("feeds", FeedViewSet)

app_name = "api"
urlpatterns = router.urls
