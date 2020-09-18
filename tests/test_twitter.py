import os

import pytest

from advertools.twitter import *
from advertools.twitter import FUNCTIONS
from advertools.twitter import _get_counts

app_key = os.environ.get('APP_KEY')
app_secret = os.environ.get('APP_SECRET')
oauth_token = os.environ.get('OAUTH_TOKEN')
oauth_token_secret = os.environ.get('OAUTH_TOKEN_SECRET')

auth_params = {
    'app_key': app_key,
    'app_secret': app_secret,
    'oauth_token': oauth_token,
    'oauth_token_secret': oauth_token_secret,
}


set_auth_params(**auth_params)

skip_api_tests = pytest.mark.skipif(os.environ.get('ADV_TEST_OFFLINE'),
                                    reason='Run all except API dependents')

def test_get_counts():
    for i in [None, 13, 70, 100, 101, 200, 578]:
        result = _get_counts(i, 100)
        assert sum(result) == i if i is not None else 100
        assert 0 not in result


def test_set_auth_params():
    set_auth_params(**auth_params)
    for func in FUNCTIONS:
        assert func.get_auth_params()['app_key'] == app_key
        assert func.get_auth_params()['app_secret'] == app_secret
        assert func.get_auth_params()['oauth_token'] == oauth_token
        assert func.get_auth_params()['oauth_token_secret'] == oauth_token_secret


@skip_api_tests
def test_get_application_rate_limit_status():
    for truth in [True, False]:
        result = get_application_rate_limit_status(truth)
        assert type(result) == pd.core.frame.DataFrame
        assert 'endpoint' in result


@skip_api_tests
def test_get_available_trends():
    result = get_available_trends()
    assert type(result) == pd.core.frame.DataFrame
    assert 'woeid' in result


@skip_api_tests
def test_get_favorites():
    result = get_favorites(screen_name='twitter', count=5,
                           tweet_mode='extended')
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert 'tweet_full_text' in result
    assert all([embd_uid == uid for embd_uid, uid in
                zip([x['id'] for x in result['tweet_user']],
                    result['user_id'])])


@skip_api_tests
def test_get_followers_ids():
    result = get_followers_ids(screen_name='nytimes', count=5)
    assert len(result['ids']) <= 5


@skip_api_tests
def test_get_followers_list():
    result = get_followers_list(screen_name='eliasdabbas', count=5,
                                skip_status=None)
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5 
    assert 'screen_name' in result


@skip_api_tests
def test_get_friends_ids():
    result = get_friends_ids(screen_name='twitter', count=5)
    assert len(result['ids']) <= 5 


@skip_api_tests
def test_get_friends_list():
    result = get_friends_list(screen_name='shakira', count=5)
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert 'screen_name' in result


@skip_api_tests
def test_get_home_timeline():
    result = get_home_timeline(count=5, tweet_mode='extended')
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert 'tweet_full_text' in result


@skip_api_tests
def test_get_list_members():
    result = get_list_members(slug='nyt-journalists',
                              owner_screen_name='nytimes', count=5)
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert 'screen_name' in result


@skip_api_tests
def test_get_list_memberships():
    result = get_list_memberships(screen_name='ThePSF', count=5)
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert 'list_full_name' in result


@skip_api_tests
def test_get_list_statuses():
    result = get_list_statuses(slug='nyt-journalists',
                               owner_screen_name='nytimes', count=5,
                               tweet_mode='extended')
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert 'tweet_full_text' in result
    assert all([embd_uid == uid for embd_uid, uid in
                zip([x['id'] for x in result['tweet_user']],
                    result['user_id'])])


@skip_api_tests
def test_get_list_subscribers():
    result = get_list_subscribers(slug='nyt-journalists',
                                  owner_screen_name='nytimes', count=5)
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5


@skip_api_tests
def test_get_list_subscriptions():
    result = get_list_subscriptions(screen_name='twitter', count=5)
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5


@skip_api_tests
def test_get_mentions_timeline():
    result = get_mentions_timeline(count=5, tweet_mode='extended')
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert 'tweet_full_text' in result
    assert all([embd_uid == uid for embd_uid, uid in
                zip([x['id'] for x in result['tweet_user']],
                    result['user_id'])])


@skip_api_tests
def test_get_place_trends():
    result = get_place_trends(ids=[23424950, 766273])
    assert type(result) == pd.core.frame.DataFrame
    assert result['location'].str.contains('Madrid|Spain').all()
    result_single_id = get_place_trends(ids=1)
    assert type(result_single_id) == pd.core.frame.DataFrame


@skip_api_tests
def test_get_retweeters_ids():
    result = get_retweeters_ids(id=1032676609902428160, count=5)
    assert len(result['ids']) <= 5


@skip_api_tests
def test_get_retweets():
    result = get_retweets(id=1032676609902428160, tweet_mode='extended', count=5)
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert all([embd_uid == uid for embd_uid, uid in
                zip([x['id'] for x in result['tweet_user']],
                    result['user_id'])])


@skip_api_tests
def test_get_supported_languages():
    result = get_supported_languages()
    assert type(result) == pd.core.frame.DataFrame
    assert 'code' in result


@skip_api_tests
def test_get_user_timeline():
    result = get_user_timeline(screen_name='bbc', count=5,
                               tweet_mode='extended')
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert 'tweet_full_text' in result
    assert 'user_id' in result
    assert all([embd_uid == uid for embd_uid, uid in
                zip([x['id'] for x in result['tweet_user']],
                    result['user_id'])])
    long_result = get_user_timeline(screen_name='eliasdabbas', count=2000,
                                    tweet_mode='extended')
    assert type(result) == pd.core.frame.DataFrame


@skip_api_tests
def test_lookup_status():
    result = lookup_status(id=[1032676609902428160,
                               1031574983095533568],
                           tweet_mode='extended')
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert all([embd_uid == uid for embd_uid, uid in
                zip([x['id'] for x in result['tweet_user']],
                    result['user_id'])])


@skip_api_tests
def test_lookup_user():
    result = lookup_user(screen_name=['twitter', 'nytimes', 'shakira'])
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 3


@skip_api_tests
def test_retweeted_of_me():
    result = retweeted_of_me(count=5, tweet_mode='extended')
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert all([embd_uid == uid for embd_uid, uid in
                zip([x['id'] for x in result['tweet_user']],
                    result['user_id'])])


@skip_api_tests
def test_search():
    result = search(q='basketball', lang='en', count=5, tweet_mode='extended')
    result_compat = search(q='basketball', lang='en', count=5,
                           tweet_mode='compat')
    assert type(result) == pd.core.frame.DataFrame
    assert type(result_compat) == pd.core.frame.DataFrame
    assert len(result) <= 5
    assert len(result_compat) <= 5
    assert 'tweet_full_text' in result
    assert 'tweet_text' in result_compat
    assert all([embd_uid == uid for embd_uid, uid in
                zip([x['id'] for x in result['tweet_user']],
                    result['user_id'])])
    assert all([embd_uid == uid for embd_uid, uid in
                zip([x['id'] for x in result['tweet_user']],
                    result['user_id'])])


@skip_api_tests
def test_search_no_error_on_empty_result():
    result = search(q='thisqueryhasnoresult!@#$%^', lang='ar',
                    count=200, tweet_mode='extended')
    assert isinstance(result, pd.core.frame.DataFrame)
    assert len(result) == 0


@skip_api_tests
def test_search_users():
    result = search_users(q='finance', count=5)
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5


@skip_api_tests
def test_show_lists():
    result = show_lists(screen_name='bbc')
    assert type(result) == pd.core.frame.DataFrame


@skip_api_tests
def test_show_owned_lists():
    result = show_owned_lists(screen_name='nytimes', count=5)
    assert type(result) == pd.core.frame.DataFrame
    assert len(result) <= 5
