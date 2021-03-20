import pytest

from django.test import Client
from django.urls import reverse

from rss_reader.feeds.views import IndexView
from rss_reader.users.models import User

pytestmark = pytest.mark.django_db

def test_index_view():
    client = Client()
    client.force_login(User.objects.create(username='testuser'))
    response = client.get(reverse('feeds:home'))

    assert response.status_code == 200
