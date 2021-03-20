from rss_reader.feeds.models import Feed

def test_is_url_valid_method():
    """
    Make sure the 'is_url_valid' method
    returns False when the passed url is
    invalid
    """
    is_valid = Feed.is_url_valid('https://a_bad_url.com')
    assert is_valid == False
