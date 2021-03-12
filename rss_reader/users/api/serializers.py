from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # foo = serializers.SerializerMethodField()
    feeds_quantity = serializers.SerializerMethodField()

    def get_feeds_quantity(self, obj):
        return obj.get_feeds_quantity()

    class Meta:
        model = User
        fields = ["username", "name", "url", "feeds_quantity"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }
