from django.contrib import admin

from .models import Feed, FeedCategory

admin.site.register(Feed)
admin.site.register(FeedCategory)
