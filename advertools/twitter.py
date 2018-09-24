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
            except TwythonRateLimitError as e:
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