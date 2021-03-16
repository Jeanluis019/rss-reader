from django.urls import reverse, resolve

def test_index():
    assert reverse('feeds:home') == '/'
    assert resolve('/').view_name == 'feeds:home'
