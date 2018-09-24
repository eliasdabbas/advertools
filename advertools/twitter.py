from functools import wraps

from twython import Twython
import pandas as pd


def authenticate(func):
    auth_params = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    def set_auth_params(**params):
        nonlocal auth_params
        auth_params.update(params)

    def get_auth_params():
        return auth_params

    wrapper.set_auth_params = set_auth_params
    wrapper.get_auth_params = get_auth_params
    return wrapper

def tweets_to_dataframe(func):
    @wraps(func)
    def wrapper(count=None, trim_user=False, *args, **kwargs):
        nonlocal func
        twtr = Twython(**wrapper.get_auth_params()) 

        func = eval('twtr.' + func.__name__)
        count = count or 15
        pages = (count // 100) + 1

        tweets_responses = []
        for i in range(pages):
            try:
                tweets = func(max_id=None if i == 0 else
                                  tweets_responses[-1]['statuses'][-1]['id'] - 1,
                              count=min([100, count]),
                              *args, **kwargs)
                tweets_responses.append(tweets)
            except Exception as e:
                break
        tweets_users_df = pd.DataFrame()
        for tweets in tweets_responses:
            if func.__name__ == 'search':
                tweets_temp = pd.DataFrame(tweets['statuses'])
            else:
                tweets_temp = pd.DataFrame(tweets)
            tweets_temp.columns = ['tweet_' + t for t in tweets_temp.columns]
            if func.__name__ == 'search':
                users_temp = pd.DataFrame([x['user'] for x in tweets['statuses']])
            else:
                users_temp = pd.DataFrame([x['user'] for x in tweets])
            users_temp.columns = ['user_' + u for u in users_temp.columns]
            tweets_users_temp = pd.concat([tweets_temp,users_temp], axis=1)
            tweets_users_df = tweets_users_df.append(tweets_users_temp,
                                                     ignore_index=True, sort=False)

        tweets_users_df['tweet_source'] = tweets_users_df['tweet_source'].str.extract('nofollow">(.*)</a>')[0]
        tweets_users_df['tweet_created_at'] = pd.to_datetime(tweets_users_df['tweet_created_at'])
        tweets_users_df['user_created_at'] = pd.to_datetime(tweets_users_df['user_created_at'])

        return tweets_users_df
    return wrapper


@tweets_to_dataframe
@authenticate
def search():
    pass


@tweets_to_dataframe
@authenticate
def get_user_timeline():
    pass


@tweets_to_dataframe
@authenticate
def get_home_timeline():
    pass


@tweets_to_dataframe
@authenticate
def get_favorites():
    pass



@tweets_to_dataframe
@authenticate
def get_list_statuses():
    pass


@tweets_to_dataframe
@authenticate
def get_mentions_timeline():
    pass


@authenticate
def get_available_trends():
    twtr = Twython(**get_available_trends.get_auth_params())

    available_trends = twtr.get_available_trends()
    trends_df = pd.DataFrame(available_trends)
    trends_df['code'] = [x['code'] for x in trends_df['placeType']]
    trends_df['place_type'] = [x['name'] for x in trends_df['placeType']]
    del trends_df['placeType']
    return trends_df


@authenticate
def get_place_trends(ids):
    twtr = Twython(**get_place_trends.get_auth_params())
    trends_df = pd.DataFrame()
    if isinstance(ids, int):
        ids = [ids]
    for place_id in ids:

        place_trends = twtr.get_place_trends(id=place_id)
        trend_df = pd.DataFrame(place_trends[0]['trends'])
        trend_df = trend_df.sort_values(['tweet_volume'], ascending=False)
        trend_df['location'] = place_trends[0]['locations'][0]['name']
        trend_df['woeid'] = place_trends[0]['locations'][0]['woeid']
        trend_df['time'] = pd.to_datetime(place_trends[0]['created_at'])

        trends_df = trends_df.append(trend_df, ignore_index=True)

    trends_df = trends_df.sort_values(['woeid', 'tweet_volume'],
                                      ascending=[True, False])
    trends_df = trends_df.reset_index(drop=True)
    return trends_df


@authenticate
def get_supported_languages():
    twtr = Twython(**get_supported_languages.get_auth_params())
    langs = twtr.get_supported_languages()
    return pd.DataFrame(langs)


FUNCTIONS = [search, get_user_timeline, get_home_timeline, get_favorites,
             get_list_statuses, get_mentions_timeline, get_available_trends,
             get_place_trends, get_supported_languages]


def set_auth_params(app_key=None, app_secret=None, oauth_token=None,
                    oauth_token_secret=None, access_token=None,
                    token_type='bearer', oauth_version=1, api_version='1.1',
                    client_args=None, auth_endpoint='authenticate'):
    params = locals()
    for func in FUNCTIONS:
        func.set_auth_params(**params)
    return None
