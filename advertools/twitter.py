"""

.. _twitter:

Twitter Data API
================
Easily connect to the Twitter API and start your analysis immediately.

Main Features:

1 **Get the results in a DataFrame**: With the exception of three functions
that return a list of ID's, everything else returns a pandas DataFrame, ready
to use. This allows you to spend more time analyzing data, and less time
figuring out the structure of the JSON response object. It's not complicated
or anything, just takes time.

2 **Manage looping and merging**: there is a limit on how many results you get
per request (typically in the 100 - 200 range), several requests have to be
made, and merged together. Not all responses have the same structure, so this
is also handled. You only have to provide the number of responses you want
through the ``count`` parameter where applicable (provided you are within
your app's rate limits).

3 **Unnesting nested objects**: Many response objects contain very rich
embedded data, which is usually meta data about the response. For example,
when you request tweets, you get a user object along with that. This is very
helpful in better understanding who made the tweet, and how
influential/credible they are.

4 **Documentation**: All available parameters are included in the function
signatures, to make it easier to explore interactively, as well as
descriptions of the parameters imported from the Twitter documentation.

Authentication
--------------

Before starting you will have to create an app through
`developer.twitter.com <https://developer.twitter.com/>`_, and then you can get
your authentication keys from your dashboard. Then you can authenticate as
follows:

.. code-block:: python

   >>> auth_params = {
   ...     'app_key': 'YOUR_APP_KEY',
   ...     'app_secret': 'YOUR_APP_SECRET',
   ... }
   >>> import advertools as adv
   >>> adv.twitter.set_auth_params(**auth_params)

In some cases, you might be required to add ``oauth_token`` and
``oauth_token_secret, which case you ``auth_params`` will look like this:

.. code-block:: python

   >>> auth_params = {
   ...     'app_key': 'YOUR_APP_KEY',
   ...     'app_secret': 'YOUR_APP_SECRET',
   ...     'oauth_token': 'YOUR_OAUTH_TOKEN',
   ...     'oauth_token_secret': 'YOUR_OAUTH_TOKEN_SECRET',
   ... }

Now every request you send will include your ``auth_params`` in it, and if
valid you will get the respective response, for example:

.. code-block:: python

   >>> python_tweets = adv.twitter.search(q='#python', tweet_mode='extended')

Make sure you always specify ``tweet_mode='extended'`` because otherwise you
will get tweets that are 140 characters long.

When you have tweets and user data in the DataFrame, the column names would be
prepended with ``tweet_`` and ``user_`` to make it clear what the data belong
to.


Functions
---------
"""

import logging
from functools import wraps

import pandas as pd
from twython import Twython

if int(pd.__version__[0]) >= 1:
    from pandas import json_normalize
else:
    from pandas.io.json import json_normalize


TWITTER_LOG_FMT = (
    "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d "
    "| %(funcName)s | %(message)s"
)
logging.basicConfig(format=TWITTER_LOG_FMT)

# Functions that depend on 'previous_cursor' and 'next_cursor' to
# navigate requests with a lot of data, request pagination basically.
CURSORED_FUNCTIONS = [
    "get_followers_ids",
    "get_followers_list",
    "get_friends_ids",
    "get_friends_list",
    "get_list_members",
    "get_list_memberships",
    "get_list_subscribers",
    "get_list_subscriptions",
    "get_retweeters_ids",
    "show_owned_lists",
]


# Responses that contain a special key (and the name of that key)
# containing the required data and need to be extracted through
# that key, as opposed to other responses where you can easily
# call DataFrame on them directly
SPECIAL_KEY_FUNCS = {
    "search": "statuses",
    "get_followers_list": "users",
    "get_friends_list": "users",
    "get_list_members": "users",
    "get_list_subscribers": "users",
    "get_list_memberships": "lists",
    "get_list_subscriptions": "lists",
    "show_owned_lists": "lists",
}


# Functions that contain an embedded ``user`` key, containing
# 40+ attributes of the user tweeting, listed, retweeted, etc.
USER_DATA_EMBEDDED = {
    "get_favorites": "tweet_",
    "get_home_timeline": "tweet_",
    "get_list_memberships": "list_",
    "get_list_statuses": "tweet_",
    "get_list_subscriptions": "",
    "get_mentions_timeline": "tweet_",
    "get_retweets": "tweet_",
    "get_user_timeline": "tweet_",
    "lookup_status": "tweet_",
    "retweeted_of_me": "tweet_",
    "search": "tweet_",
    "show_lists": "list_",
    "show_owned_lists": "list_",
}


DEFAULT_COUNTS = {
    "get_favorites": 200,
    "get_followers_ids": 5000,
    "get_followers_list": 200,
    "get_friends_ids": 5000,
    "get_friends_list": 200,
    "get_home_timeline": 200,
    "get_list_members": 5000,
    "get_list_memberships": 1000,
    "get_list_statuses": 100,
    "get_list_subscribers": 5000,
    "get_list_subscriptions": 1000,
    "get_mentions_timeline": 200,
    "get_retweeters_ids": 100,
    "get_retweets": 100,
    "get_user_timeline": 200,
    "lookup_status": 100,
    "lookup_user": 100,
    "retweeted_of_me": 100,
    "search": 100,
    "search_users": 20,
    "show_lists": 100,
    "show_owned_lists": 1000,
}


def _expand_entities(df):
    if "tweet_entities" in df:
        colnames = [
            "tweet_entities_" + x
            for x in ["mentions", "hashtags", "urls", "symbols", "media"]
        ]
        entities_df = json_normalize(df["tweet_entities"])
        mentions = [
            ", ".join(["@" + x["screen_name"] for x in y])
            for y in entities_df["user_mentions"]
        ]
        hashtags = [
            ", ".join(["#" + x["text"] for x in y]) for y in entities_df["hashtags"]
        ]
        urls = [", ".join([x["expanded_url"] for x in y]) for y in entities_df["urls"]]
        symbols = [
            ", ".join(["$" + x["text"] for x in y]) for y in entities_df["symbols"]
        ]

        if "media" in entities_df:
            entities_df["media"] = entities_df["media"].fillna("")
            media = [
                ", ".join([x["media_url"] for x in y]) if y != "" else y
                for y in entities_df["media"]
            ]
            entity_cols = [mentions, hashtags, urls, symbols, media]
        else:
            entity_cols = [mentions, hashtags, urls, symbols]
        col_idx = df.columns.get_loc("tweet_entities")
        for j, col in enumerate(entity_cols):
            df.insert(col_idx + j + 1, colnames[j], col)
    return df


def _get_counts(number=None, default=None):
    """Split a number into a list of divisors and the remainder.
    The divisor is the default count in this case."""
    if not number:
        number = 1
    div = divmod(number, default)
    result = [default for x in range(div[0])]
    if div[1] != 0:
        return result + [div[1]]
    return result


def make_dataframe(func):
    @wraps(func)
    def wrapper(count=None, max_id=None, *args, **kwargs):
        nonlocal func

        twtr = Twython(**wrapper.get_auth_params())  # noqa: F841
        fname = func.__name__
        func = eval("twtr." + fname)

        if count is None:
            count = DEFAULT_COUNTS[fname]
        counts = _get_counts(count, DEFAULT_COUNTS[fname])

        responses = []
        for i, count in enumerate(counts):
            if fname == "search":
                if responses and not responses[-1]["statuses"]:
                    break
                max_id = (
                    (max_id or None)
                    if i == 0
                    else (responses[-1]["statuses"][-1]["id"] - 1)
                )
            if (fname != "search") and (fname not in CURSORED_FUNCTIONS):
                if responses and len(responses[-1]) == 0:
                    break
                max_id = (max_id or None) if i == 0 else (responses[-1][-1]["id"] - 1)
            if fname in CURSORED_FUNCTIONS:
                cursor = None if i == 0 else responses[-1]["next_cursor"]
                max_id = None
            else:
                cursor = None
            kwargs_log = ", ".join([k + "=" + str(v) for k, v in kwargs.items()])
            args_log = ", ".join(args)
            logging.info(
                msg=fname
                + " | "
                + "Requesting: "
                + "count="
                + str(count)
                + ", max_id="
                + str(max_id)
                + ", "
                + kwargs_log
                + args_log
            )

            resp = func(count=count, max_id=max_id, cursor=cursor, *args, **kwargs)  # noqa: B026
            responses.append(resp)

        if "_ids" in fname:
            finallist = []
            for sublist in responses:
                finallist.extend(sublist["ids"])
            finaldict = {
                "previous_cursor": responses[0]["previous_cursor"],
                "next_cursor": responses[-1]["next_cursor"],
                "ids": finallist,
            }
            return finaldict

        final_df = pd.DataFrame()
        for resp in responses:
            if SPECIAL_KEY_FUNCS.get(fname):
                resp_df = pd.DataFrame(resp[SPECIAL_KEY_FUNCS.get(fname)])
                if fname in USER_DATA_EMBEDDED:
                    resp_df.columns = [
                        USER_DATA_EMBEDDED[fname] + col for col in resp_df.columns
                    ]
                    user_df = pd.DataFrame(
                        [x["user"] for x in resp[SPECIAL_KEY_FUNCS.get(fname)]]
                    )
                    user_df.columns = ["user_" + col for col in user_df.columns]
                    temp_df = pd.concat([resp_df, user_df], axis=1, sort=False)
                else:
                    temp_df = resp_df
            else:
                resp_df = pd.DataFrame(resp)

                if fname in USER_DATA_EMBEDDED:
                    resp_df.columns = [
                        USER_DATA_EMBEDDED[fname] + x for x in resp_df.columns
                    ]
                    user_df = pd.DataFrame([x["user"] for x in resp])
                    user_df.columns = ["user_" + x for x in user_df.columns]
                    temp_df = pd.concat([resp_df, user_df], axis=1)
                else:
                    temp_df = resp_df
            final_df = pd.concat([final_df, temp_df], sort=False, ignore_index=True)

        for col in final_df:
            if "created_at" in col:
                final_df[col] = pd.to_datetime(final_df[col])
        for col in final_df:
            if "source" in col:
                final_df[col + "_url"] = final_df[col].str.extract(
                    '<a href="(.*)" rel='
                )[0]
                final_df[col] = final_df[col].str.extract('nofollow">(.*)</a>')[0]
        if "tweet_entities" in final_df:
            return _expand_entities(final_df)

        return final_df

    return wrapper


def authenticate(func):
    """Used internally, please use set_auth_params for authentication."""
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


@authenticate
def get_application_rate_limit_status(consumed_only=True):
    """
    Returns the current rate limits for methods belonging to the
        specified resource families.

    :param consumed_only: Whether or not to return only items that
        have been consumed. Otherwise returns the full list.

    https://developer.twitter.com/en/docs/developer-utilities/rate-limit-status/api-reference/get-application-rate_limit_status
    """
    twtr = Twython(**get_application_rate_limit_status.get_auth_params())
    ratelimit = twtr.get_application_rate_limit_status()
    limit_df = pd.DataFrame()
    for resource in ratelimit["resources"]:
        temp_df = pd.DataFrame(ratelimit["resources"][resource]).T
        limit_df = pd.concat([limit_df, temp_df], sort=False)
    limit_df["reset"] = pd.to_datetime(limit_df["reset"], unit="s")
    limit_df["resource"] = limit_df.index.str.split("/").str[1]
    limit_df.index.name = "endpoint"
    limit_df = limit_df.sort_values(["resource"])
    limit_df = limit_df.reset_index()
    if consumed_only:
        print(
            " " * 12,
            "Rate limit as of:",
            pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%-d %H:%M:%S"),
        )
        return limit_df[limit_df["limit"].ne(limit_df["remaining"])]
    return limit_df


@authenticate
def get_available_trends():
    """
    Returns the locations that Twitter has trending topic information for.

    https://developer.twitter.com/en/docs/trends/locations-with-trending-topics/api-reference/get-trends-available
    """
    twtr = Twython(**get_available_trends.get_auth_params())

    available_trends = twtr.get_available_trends()
    trends_df = pd.DataFrame(available_trends)
    trends_df["code"] = [x["code"] for x in trends_df["placeType"]]
    trends_df["place_type"] = [x["name"] for x in trends_df["placeType"]]
    del trends_df["placeType"]
    trends_df = trends_df.sort_values(["country", "place_type", "name"])
    trends_df = trends_df.reset_index(drop=True)
    return trends_df


@make_dataframe
@authenticate
def get_favorites(
    user_id=None,
    screen_name=None,
    count=None,
    since_id=None,
    max_id=None,
    include_entities=None,
    tweet_mode=None,
):
    """
    Returns the 20 most recent Tweets favorited by the authenticating
        or specified user.

    :param user_id: (int - optional) The ID of the user for whom to return
        results.
    :param screen_name: (str - optional) The screen name of the user for whom
        to return results.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param since_id: (int - optional) Returns results with an ID greater than
        (that is, more recent than) the specified ID. There are limits to the number of
        Tweets which can be accessed through the API. If the limit of Tweets has
        occured since the since_id, the since_id will be forced to the oldest ID
        available.
    :param max_id: (int - optional) Returns results with an ID less than (that
        is, older than) or equal to the specified ID.
    :param include_entities: (bool - optional) The entities node will be
        omitted when set to False .
    :param tweet_mode: (str - optional) Valid request values are compat and
        extended, which give compatibility mode and extended mode, respectively for
        Tweets that contain over 140 characters

    https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-favorites-list
    """
    pass


@make_dataframe
@authenticate
def get_followers_ids(
    user_id=None, screen_name=None, cursor=None, stringify_ids=None, count=None
):
    """
    Returns a cursored collection of user IDs for every user
        following the specified user.

    :param user_id: (int - optional) The ID of the user for whom to return
        results.
    :param screen_name: (str - optional) The screen name of the user for whom
        to return results.
    :param cursor: (cursor - semi-optional) Causes the list of connections to
        be broken into pages of no more than 5000 IDs at a time. The number of IDs
        returned is not guaranteed to be 5000 as suspended users are filtered out after
        connections are queried. If no cursor is provided, a value of -1 will be
        assumed, which is the first “page.” The response from the API will include a
        previous_cursor and next_cursor to allow paging back and forth. See Using
        cursors to navigate collections for more information.
    :param stringify_ids: (bool - optional) Some programming environments will
        not consume Twitter IDs due to their size. Provide this option to have IDs
        returned as strings instead. More about Twitter IDs.
    :param count: (int - optional) Specifies the number of results to retrieve.

    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-followers-ids
    """
    pass


@make_dataframe
@authenticate
def get_followers_list(
    user_id=None,
    screen_name=None,
    cursor=None,
    count=None,
    skip_status=None,
    include_user_entities=None,
):
    """
    Returns a cursored collection of user objects for users
        following the specified user.

    :param user_id: (int - optional) The ID of the user for whom to return
        results.
    :param screen_name: (str - optional) The screen name of the user for whom
        to return results.
    :param cursor: (cursor - semi-optional) Causes the results to be broken
        into pages. If no cursor is provided, a value of -1 will be assumed, which is
        the first “page.” The response from the API will include a previous_cursor and
        next_cursor to allow paging back and forth. See Using cursors to navigate
        collections for more information.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param skip_status: (bool - optional) When set to True, statuses will not
        be included in the returned user objects. If set to any other value, statuses
        will be included.
    :param include_user_entities: (bool - optional) The user object entities
        node will not be included when set to False.

    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-followers-list
    """
    pass


@make_dataframe
@authenticate
def get_friends_ids(
    user_id=None, screen_name=None, cursor=None, stringify_ids=None, count=None
):
    """
    Returns a cursored collection of user IDs for every user the
        specified user is following (otherwise known as their "friends").

    :param user_id: (int - optional) The ID of the user for whom to return
        results.
    :param screen_name: (str - optional) The screen name of the user for whom
        to return results.
    :param cursor: (cursor - semi-optional) Causes the list of connections to
        be broken into pages of no more than 5000 IDs at a time. The number of IDs
        returned is not guaranteed to be 5000 as suspended users are filtered out after
        connections are queried. If no cursor is provided, a value of -1 will be
        assumed, which is the first “page.” The response from the API will include a
        previous_cursor and next_cursor to allow paging back and forth. See Using
        cursors to navigate collections for more information.
    :param stringify_ids: (bool - optional) Some programming environments will
        not consume Twitter IDs due to their size. Provide this option to have IDs
        returned as strings instead. More about Twitter IDs.
    :param count: (int - optional) Specifies the number of results to retrieve.

    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friends-ids
    """
    pass


@make_dataframe
@authenticate
def get_friends_list(
    user_id=None,
    screen_name=None,
    cursor=None,
    count=None,
    skip_status=None,
    include_user_entities=None,
):
    """
    Returns a cursored collection of user objects for every user the
        specified user is following (otherwise known as their "friends").

    :param user_id: (int - optional) The ID of the user for whom to return
        results.
    :param screen_name: (str - optional) The screen name of the user for whom
        to return results.
    :param cursor: (cursor - semi-optional) Causes the results to be broken
        into pages. If no cursor is provided, a value of -1 will be assumed, which is
        the first “page.” The response from the API will include a previous_cursor and
        next_cursor to allow paging back and forth. See Using cursors to navigate
        collections for more information.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param skip_status: (bool - optional) When set to True statuses will not be
        included in the returned user objects.
    :param include_user_entities: (bool - optional) The user object entities
        node will not be included when set to False.

    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friends-list
    """
    pass


@make_dataframe
@authenticate
def get_home_timeline(
    count=None,
    since_id=None,
    max_id=None,
    trim_user=None,
    exclude_replies=None,
    include_entities=None,
    tweet_mode=None,
):
    """
    Returns a collection of the most recent Tweets and retweets
        posted by the authenticating user and the users they follow.

    :param count: (int - optional) Specifies the number of results to retrieve.
    :param since_id: (int - optional) Returns results with an ID greater than
        (that is, more recent than) the specified ID. There are limits to the number of
        Tweets which can be accessed through the API. If the limit of Tweets has
        occured since the since_id, the since_id will be forced to the oldest ID
        available.
    :param max_id: (int - optional) Returns results with an ID less than (that
        is, older than) or equal to the specified ID.
    :param trim_user: (bool - optional) When set to True, each Tweet returned
        in a timeline will include a user object including only the status authors
        numerical ID. Omit this parameter to receive the complete user object.
    :param exclude_replies: (bool - optional) This parameter will prevent
        replies from appearing in the returned timeline. Using exclude_replies with the
        count parameter will mean you will receive up-to count Tweets — this is because
        the count parameter retrieves that many Tweets before filtering out retweets
        and replies.
    :param include_entities: (bool - optional) The entities node will not be
        included when set to False.
    :param tweet_mode: (str - optional) Valid request values are compat and
        extended, which give compatibility mode and extended mode, respectively for
        Tweets that contain over 140 characters

    https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-home_timeline
    """
    pass


@make_dataframe
@authenticate
def get_list_members(
    list_id=None,
    slug=None,
    owner_screen_name=None,
    owner_id=None,
    count=None,
    cursor=None,
    include_entities=None,
    skip_status=None,
):
    """
    Returns the members of the specified list.

    :param list_id: (str - required) The numerical id of the list.
    :param slug: (str - required) You can identify a list by its slug instead
        of its numerical id. If you decide to do so, note that you’ll also have to
        specify the list owner using the owner_id or owner_screen_name parameters.
    :param owner_screen_name: (str - optional) The screen name of the user who
        owns the list being requested by a slug.
    :param owner_id: (int - optional) The user ID of the user who owns the list
        being requested by a slug.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param cursor: (cursor - semi-optional) Causes the collection of list
        members to be broken into “pages” of consistent sizes (specified by the count
        parameter). If no cursor is provided, a value of -1 will be assumed, which is
        the first “page.” The response from the API will include a previous_cursor and
        next_cursor to allow paging back and forth. See Using cursors to navigate
        collections for more information.
    :param include_entities: (bool - optional) The entities node will not be
        included when set to False.
    :param skip_status: (bool - optional) When set to True statuses will not be
        included in the returned user objects.

    https://developer.twitter.com/en/docs/accounts-and-users/create-manage-lists/api-reference/get-lists-members
    """
    pass


@make_dataframe
@authenticate
def get_list_memberships(
    user_id=None, screen_name=None, count=None, cursor=None, filter_to_owned_lists=None
):
    """
    Returns the lists the specified user has been added to.

    :param user_id: (int - optional) The ID of the user for whom to return
        results. Helpful for disambiguating when a valid user ID is also a valid screen
        name.
    :param screen_name: (str - optional) The screen name of the user for whom
        to return results. Helpful for disambiguating when a valid screen name is also
        a user ID.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param cursor: (cursor - optional) Breaks the results into pages. Provide a
        value of -1 to begin paging. Provide values as returned in the response body’s
        next_cursor and previous_cursor attributes to page back and forth in the list.
        It is recommended to always use cursors when the method supports them. See
        Cursoring for more information.
    :param filter_to_owned_lists: (bool - optional) When True, will return just
        lists the authenticating user owns, and the user represented by user_id or
        screen_name is a member of.

    https://developer.twitter.com/en/docs/accounts-and-users/create-manage-lists/api-reference/get-lists-memberships
    """
    pass


@make_dataframe
@authenticate
def get_list_statuses(
    list_id=None,
    slug=None,
    owner_screen_name=None,
    owner_id=None,
    since_id=None,
    max_id=None,
    count=None,
    include_entities=None,
    include_rts=None,
    tweet_mode=None,
):
    """
    Returns a timeline of tweets authored by members of the specified list.

    :param list_id: (str - required) The numerical id of the list.
    :param slug: (str - required) You can identify a list by its slug instead
        of its numerical id. If you decide to do so, note that you’ll also have to
        specify the list owner using the owner_id or owner_screen_name parameters.
    :param owner_screen_name: (str - optional) The screen name of the user who
        owns the list being requested by a slug .
    :param owner_id: (int - optional) The user ID of the user who owns the list
        being requested by a slug .
    :param since_id: (int - optional) Returns results with an ID greater than
        (that is, more recent than) the specified ID. There are limits to the number of
        Tweets which can be accessed through the API. If the limit of Tweets has
        occured since the since_id, the since_id will be forced to the oldest ID
        available.
    :param max_id: (int - optional) Returns results with an ID less than (that
        is, older than) or equal to the specified ID.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param include_entities: (bool - optional) Entities are ON by default in
        API 1.1, each tweet includes a node called “entities”. This node offers a
        variety of metadata about the tweet in a discreet structure, including:
        user_mentions, urls, and hashtags. You can omit entities from the result by
        using include_entities=False
    :param include_rts: (bool - optional) When set to True, the list timeline
        will contain native retweets (if they exist) in addition to the standard stream
        of tweets. The output format of retweeted tweets is identical to the
        representation you see in home_timeline.
    :param tweet_mode: (str - optional) Valid request values are compat and
        extended, which give compatibility mode and extended mode, respectively for
        Tweets that contain over 140 characters

    https://developer.twitter.com/en/docs/accounts-and-users/create-manage-lists/api-reference/get-lists-statuses
    """
    pass


@make_dataframe
@authenticate
def get_list_subscribers(
    list_id=None,
    slug=None,
    owner_screen_name=None,
    owner_id=None,
    count=None,
    cursor=None,
    include_entities=None,
    skip_status=None,
):
    """
    Returns the subscribers of the specified list.

    :param list_id: (str - required) The numerical id of the list.
    :param slug: (str - required) You can identify a list by its slug instead
        of its numerical id. If you decide to do so, note that you’ll also have to
        specify the list owner using the owner_id or owner_screen_name parameters.
    :param owner_screen_name: (str - optional) The screen name of the user who
        owns the list being requested by a slug .
    :param owner_id: (int - optional) The user ID of the user who owns the list
        being requested by a slug .
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param cursor: (cursor - optional) Breaks the results into pages. A single
        page contains 20 lists. Provide a value of -1 to begin paging. Provide values
        as returned in the response body’s next_cursor and previous_cursor attributes
        to page back and forth in the list. See Using cursors to navigate collections
        for more information.
    :param include_entities: (bool - optional) When set to True, each tweet
        will include a node called “entities”. This node offers a variety of metadata
        about the tweet in a discreet structure, including: user_mentions, urls, and
        hashtags. While entities are opt-in on timelines at present, they will be made
        a default component of output in the future. See Tweet Entities for more
        details.
    :param skip_status: (bool - optional) When set to Truestatuses will not be
        included in the returned user objects.

    https://developer.twitter.com/en/docs/accounts-and-users/create-manage-lists/api-reference/get-lists-subscribers
    """
    pass


@make_dataframe
@authenticate
def get_list_subscriptions(user_id=None, screen_name=None, count=None, cursor=None):
    """
    Obtain a collection of the lists the specified user is subscribed to.

    :param user_id: (int - optional) The ID of the user for whom to return
        results. Helpful for disambiguating when a valid user ID is also a valid screen
        name.
    :param screen_name: (str - optional) The screen name of the user for whom
        to return results. Helpful for disambiguating when a valid screen name is also
        a user ID.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param cursor: (cursor - optional) Breaks the results into pages. Provide a
        value of -1 to begin paging. Provide values as returned in the response body’s
        next_cursor and previous_cursor attributes to page back and forth in the list.
        It is recommended to always use cursors when the method supports them. See
        Cursoring for more information.

    https://developer.twitter.com/en/docs/accounts-and-users/create-manage-lists/api-reference/get-lists-subscriptions
    """
    pass


@make_dataframe
@authenticate
def get_mentions_timeline(
    count=None,
    since_id=None,
    max_id=None,
    trim_user=None,
    include_entities=None,
    tweet_mode=None,
):
    """
    Returns the 20 most recent mentions (tweets containing a users's
        @screen_name) for the authenticating user.

    :param count: (int - optional) Specifies the number of results to retrieve.
    :param since_id: (int - optional) Returns results with an ID greater than
        (that is, more recent than) the specified ID. There are limits to the number of
        Tweets which can be accessed through the API. If the limit of Tweets has
        occured since the since_id, the since_id will be forced to the oldest ID
        available.
    :param max_id: (int - optional) Returns results with an ID less than (that
        is, older than) or equal to the specified ID.
    :param trim_user: (bool - optional) When set to True, each tweet returned
        in a timeline will include a user object including only the status authors
        numerical ID. Omit this parameter to receive the complete user object.
    :param include_entities: (bool - optional) The entities node will not be
        included when set to False.
    :param tweet_mode: (str - optional) Valid request values are compat and
        extended, which give compatibility mode and extended mode, respectively for
        Tweets that contain over 140 characters

    https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-mentions_timeline
    """
    pass


@authenticate
def get_place_trends(ids, exclude=None):
    """
    Returns the top 10 trending topics for a specific WOEID, if
        trending information is available for it.

    :param id: (int or list of ints - required) run ``get_available_trends()`` for
        the full listing.
        The Yahoo! Where On Earth ID of the
        location to return trending information for. Global information is available
        by using 1 as the WOEID .
    :param exclude: (str - optional) Setting this equal to hashtags will remove
        all hashtags from the trends list.

    https://developer.twitter.com/en/docs/trends/trends-for-location/api-reference/get-trends-place
    """
    twtr = Twython(**get_place_trends.get_auth_params())
    trends_df = pd.DataFrame()
    if isinstance(ids, int):
        ids = [ids]
    for place_id in ids:
        place_trends = twtr.get_place_trends(id=place_id)
        trend_df = pd.DataFrame(place_trends[0]["trends"])
        trend_df = trend_df.sort_values(["tweet_volume"], ascending=False)
        trend_df["location"] = place_trends[0]["locations"][0]["name"]
        trend_df["woeid"] = place_trends[0]["locations"][0]["woeid"]
        trend_df["time"] = pd.to_datetime(place_trends[0]["created_at"])

        trends_df = pd.concat([trends_df, trend_df], ignore_index=True)

    trends_df = trends_df.sort_values(
        ["woeid", "tweet_volume"], ascending=[True, False]
    )
    trends_df = trends_df.reset_index(drop=True)
    available = get_available_trends()
    available = available[["country", "parentid", "woeid", "place_type"]]
    final_df = pd.merge(trends_df, available, on="woeid")
    final_df["local_rank"] = final_df.groupby("woeid")["tweet_volume"].rank(
        method="dense", ascending=False
    )
    final_df["country_rank"] = final_df.groupby("country")["tweet_volume"].rank(
        method="dense", ascending=False
    )
    final_df = final_df[
        [
            "name",
            "location",
            "tweet_volume",
            "local_rank",
            "country",
            "country_rank",
            "time",
            "place_type",
            "promoted_content",
            "woeid",
            "parentid",
        ]
    ]
    return final_df


@make_dataframe
@authenticate
def get_retweeters_ids(id, count=None, cursor=None, stringify_ids=None):
    """
    Returns a collection of up to 100 user IDs belonging to users who
        have retweeted the tweet specified by the ``id`` parameter.
        It's better to use get_retweets because passing a count > 100
        will only get you duplicated data. 100 is the maximum even
        if there were more retweeters.

    :param id: (int - required) The numerical ID of the desired status.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param cursor: (cursor - semi-optional) Causes the list of IDs to be broken
        into pages of no more than 100 IDs at a time. The number of IDs returned is not
        guaranteed to be 100 as suspended users are filtered out after connections are
        queried. If no cursor is provided, a value of -1 will be assumed, which is the
        first “page.” The response from the API will include a previous_cursor and
        next_cursor to allow paging back and forth. See our cursor docs for more
        information. While this method supports the cursor parameter, the entire result
        set can be returned in a single cursored collection. Using the count parameter
        with this method will not provide segmented cursors for use with this
        parameter.
    :param stringify_ids: (bool - optional) Many programming environments will
        not consume Tweet ids due to their size. Provide this option to have ids
        returned as strings instead.

    https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-retweeters-ids
    """
    pass


@make_dataframe
@authenticate
def get_retweets(id, trim_user=None, tweet_mode=None):
    """
    Returns up to 100 of the first retweets of a given tweet.

    :param id: (int - required) The numerical ID of the desired status.
    :param trim_user: (bool - optional) When set to True, each tweet returned
        in a timeline will include a user object including only the status authors
        numerical ID. Omit this parameter to receive the complete user object.
    :param tweet_mode: (str - optional) Valid request values are compat and
        extended, which give compatibility mode and extended mode, respectively for
        Tweets that contain over 140 characters

    https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/post-statuses-retweet-id
    """
    pass


@authenticate
def get_supported_languages():
    """
    Returns the list of languages supported by Twitter along with
        their ISO 639-1 code.

    https://developer.twitter.com/en/docs/developer-utilities/supported-languages/api-reference/get-help-languages
    """
    twtr = Twython(**get_supported_languages.get_auth_params())
    langs = twtr.get_supported_languages()
    return pd.DataFrame(langs)


@make_dataframe
@authenticate
def get_user_timeline(
    user_id=None,
    screen_name=None,
    since_id=None,
    count=None,
    max_id=None,
    trim_user=None,
    exclude_replies=None,
    include_rts=None,
    tweet_mode=None,
):
    """
    Returns a collection of the most recent Tweets posted by the user
        indicated by the ``screen_name`` or ``user_id`` parameters.

    :param user_id: (int - optional) The ID of the user for whom to return
        results.
    :param screen_name: (str - optional) The screen name of the user for whom
        to return results.
    :param since_id: (int - optional) Returns results with an ID greater than
        (that is, more recent than) the specified ID. There are limits to the number of
        Tweets that can be accessed through the API. If the limit of Tweets has occured
        since the since_id, the since_id will be forced to the oldest ID available.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param max_id: (int - optional) Returns results with an ID less than (that
        is, older than) or equal to the specified ID.
    :param trim_user: (bool - optional) When set to True, each Tweet returned
        in a timeline will include a user object including only the status authors
        numerical ID. Omit this parameter to receive the complete user object.
    :param exclude_replies: (bool - optional) This parameter will prevent
        replies from appearing in the returned timeline. Using exclude_replies with the
        count parameter will mean you will receive up-to count tweets — this is because
        the count parameter retrieves that many Tweets before filtering out retweets
        and replies.
    :param include_rts: (bool - optional) When set to False , the timeline will
        strip any native retweets (though they will still count toward both the maximal
        length of the timeline and the slice selected by the count parameter). Note: If
        you’re using the trim_user parameter in conjunction with include_rts, the
        retweets will still contain a full user object.
    :param tweet_mode: (str - optional) Valid request values are compat and
        extended, which give compatibility mode and extended mode, respectively for
        Tweets that contain over 140 characters

    https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
    """
    pass


@make_dataframe
@authenticate
def lookup_status(
    id,
    include_entities=None,
    trim_user=None,
    map=None,
    include_ext_alt_text=None,
    include_card_uri=None,
    tweet_mode=None,
):
    """
    Returns fully-hydrated tweet objects for up to 100 tweets per
        request, as specified by comma-separated values passed to the ``id``
        parameter.

    :param id: (int - required) A comma separated list of Tweet IDs, up to 100
        are allowed in a single request.
    :param include_entities: (bool - optional) The entities node that may
        appear within embedded statuses will not be included when set to False.
    :param trim_user: (bool - optional) When set to True, each Tweet returned
        in a timeline will include a user object including only the status authors
        numerical ID. Omit this parameter to receive the complete user object.
    :param map: (bool - optional) When using the map parameter, Tweets that do
        not exist or cannot be viewed by the current user will still have their key
        represented but with an explicitly null value paired with it
    :param include_ext_alt_text: (bool - optional) If alt text has been added
        to any attached media entities, this parameter will return an ext_alt_text
        value in the top-level key for the media entity. If no value has been set, this
        will be returned as null
    :param include_card_uri: (bool - optional) When set to True, each Tweet
        returned will include a card_uri attribute when there is an ads card attached
        to the Tweet and when that card was attached using the card_uri value.
    :param tweet_mode: (str - optional) Valid request values are compat and
        extended, which give compatibility mode and extended mode, respectively for
        Tweets that contain over 140 characters

    https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-lookup
    """
    pass


@make_dataframe
@authenticate
def lookup_user(screen_name=None, user_id=None, include_entities=None, tweet_mode=None):
    """
    Returns fully-hydrated user objects for up to 100 users per request,
        as specified by comma-separated values passed to the ``user_id`` and/or
        ``screen_name`` parameters.

    :param screen_name: (str - optional) A comma separated list of screen
        names, up to 100 are allowed in a single request. You are strongly encouraged
        to use a POST for larger (up to 100 screen names) requests.
    :param user_id: (int - optional) A comma separated list of user IDs, up to
        100 are allowed in a single request. You are strongly encouraged to use a POST
        for larger requests.
    :param include_entities: (bool - optional) The entities node that may
        appear within embedded statuses will not be included when set to False.
    :param tweet_mode: (str - optional) Valid request values are compat and
        extended, which give compatibility mode and extended mode, respectively for
        Tweets that contain over 140 characters

    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup
    """
    pass


@make_dataframe
@authenticate
def retweeted_of_me(
    count=None,
    since_id=None,
    max_id=None,
    trim_user=None,
    include_entities=None,
    include_user_entities=None,
    tweet_mode=None,
):
    """
    Returns the most recent tweets authored by the authenticating user
        that have been retweeted by others.

    :param count: (int - optional) Specifies the number of results to retrieve.
    :param since_id: (int - optional) Returns results with an ID greater than
        (that is, more recent than) the specified ID. There are limits to the number of
        Tweets which can be accessed through the API. If the limit of Tweets has
        occured since the since_id, the since_id will be forced to the oldest ID
        available.
    :param max_id: (int - optional) Returns results with an ID less than (that
        is, older than) or equal to the specified ID.
    :param trim_user: (bool - optional) When set to True, each tweet returned
        in a timeline will include a user object including only the status authors
        numerical ID. Omit this parameter to receive the complete user object.
    :param include_entities: (bool - optional) The tweet entities node will not
        be included when set to False .
    :param include_user_entities: (bool - optional) The user entities node will
        not be included when set to False .
    :param tweet_mode: (str - optional) Valid request values are compat and
        extended, which give compatibility mode and extended mode, respectively for
        Tweets that contain over 140 characters

    https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-retweets_of_me
    """
    pass


@make_dataframe
@authenticate
def search(
    q,
    geocode=None,
    lang=None,
    locale=None,
    result_type=None,
    count=None,
    until=None,
    since_id=None,
    max_id=None,
    include_entities=None,
    tweet_mode=None,
):
    """
    Returns a collection of relevant Tweets matching a specified query.

    :param q: (str - required) A UTF-8, URL-encoded search query of 500
        characters maximum, including operators. Queries may additionally be limited by
        complexity.
    :param geocode: (lat lon dist - optional) Returns tweets by users located
        within a given radius of the given latitude/longitude. The location is
        preferentially taking from the Geotagging API, but will fall back to their
        Twitter profile. The parameter value is specified by ”
        latitude,longitude,radius “, where radius units must be specified as either ”
        mi ” (miles) or ” km ” (kilometers). Note that you cannot use the near operator
        via the API to geocode arbitrary locations; however you can use this geocode
        parameter to search near geocodes directly. A maximum of 1,000 distinct “sub-
        regions” will be considered when using the radius modifier.
    :param lang: (str - optional) Restricts tweets to the given language, given
        by an ISO 639-1 code. Language detection is best-effort.
    :param locale: (str - optional) Specify the language of the query you are
        sending (only ja is currently effective). This is intended for language-
        specific consumers and the default should work in the majority of cases.
    :param result_type: (str - optional) Optional. Specifies what type of
        search results you would prefer to receive. The current default is “mixed.”
        Valid values include: * mixed : Include both popular and real time results in
        the response. * recent : return only the most recent results in the response *
        popular : return only the most popular results in the response.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param until: (date - optional) Returns tweets created before the given
        date. Date should be formatted as YYYY-MM-DD. Keep in mind that the search
        index has a 7-day limit. In other words, no tweets will be found for a date
        older than one week.
    :param since_id: (int - optional) Returns results with an ID greater than
        (that is, more recent than) the specified ID. There are limits to the number of
        Tweets which can be accessed through the API. If the limit of Tweets has
        occured since the since_id, the since_id will be forced to the oldest ID
        available.
    :param max_id: (int - optional) Returns results with an ID less than (that
        is, older than) or equal to the specified ID.
    :param include_entities: (bool - optional) The entities node will not be
        included when set to False.
    :param tweet_mode: (str - optional) Valid request values are compat and
        extended, which give compatibility mode and extended mode, respectively for
        Tweets that contain over 140 characters

    +------------------------------------+-----------------------------------------------------+
    |                           Operator | Finds Tweets...                                     |
    +====================================+=====================================================+
    |                      watching now  | containing both “watching” and “now”. This is the   |
    |                                    | default operator.                                   |
    +------------------------------------+-----------------------------------------------------+
    |                      “happy hour”  |  containing the exact phrase “happy hour”.          |
    +------------------------------------+-----------------------------------------------------+
    |                      love OR hate  |  containing either “love” or “hate” (or both).      |
    +------------------------------------+-----------------------------------------------------+
    |                        beer -root  |  containing “beer” but not “root”.                  |
    +------------------------------------+-----------------------------------------------------+
    |                            #haiku  |  containing the hashtag “haiku”.                    |
    +------------------------------------+-----------------------------------------------------+
    |                     from:interior  |  sent from Twitter account “interior”.              |
    +------------------------------------+-----------------------------------------------------+
    | list:NASA/astronauts-in-space-now  | sent from a Twitter account in the NASA list        |
    |                                    | astronauts-in-space-now                             |
    +------------------------------------+-----------------------------------------------------+
    |                           to:NASA  | a Tweet authored in reply to Twitter account        |
    |                                    | “NASA”.                                             |
    +------------------------------------+-----------------------------------------------------+
    |                             @NASA  |  mentioning Twitter account “NASA”.                 |
    +------------------------------------+-----------------------------------------------------+
    |              politics filter:safe  | containing “politics” with Tweets marked as         |
    |                                    | potentially sensitive removed.                      |
    +------------------------------------+-----------------------------------------------------+
    |                puppy filter:media  |  containing “puppy” and an image or video.          |
    +------------------------------------+-----------------------------------------------------+
    |            puppy -filter:retweets  |  containing “puppy”, filtering out retweets         |
    +------------------------------------+-----------------------------------------------------+
    |         puppy filter:native_video  | containing “puppy” and an uploaded video, Amplify   |
    |                                    | video, Periscope, or Vine.                          |
    +------------------------------------+-----------------------------------------------------+
    |            puppy filter:periscope  |  containing “puppy” and a Periscope video URL.      |
    +------------------------------------+-----------------------------------------------------+
    |                 puppy filter:vine  |  containing “puppy” and a Vine.                     |
    +------------------------------------+-----------------------------------------------------+
    |               puppy filter:images  | containing “puppy” and links identified as photos,  |
    |                                    | including third parties such as Instagram.          |
    +------------------------------------+-----------------------------------------------------+
    |                puppy filter:twimg  | containing “puppy” and a pic.twitter.com link       |
    |                                    | representing one or more photos.                    |
    +------------------------------------+-----------------------------------------------------+
    |            hilarious filter:links  |  containing “hilarious” and linking to URL.         |
    +------------------------------------+-----------------------------------------------------+
    |                  puppy url:amazon  | containing “puppy” and a URL with the word          |
    |                                    | “amazon” anywhere within it.                        |
    +------------------------------------+-----------------------------------------------------+
    |        superhero since:2015-12-21  | containing “superhero” and sent since date          |
    |                                    | “2015-12-21” (year-month-day).                      |
    +------------------------------------+-----------------------------------------------------+
    |            puppy until:2015-12-21  | containing “puppy” and sent before the date         |
    |                                    | “2015-12-21”.                                       |
    +------------------------------------+-----------------------------------------------------+
    |                   movie -scary :)  | containing “movie”, but not “scary”, and with a     |
    |                                    | positive attitude.                                  |
    +------------------------------------+-----------------------------------------------------+
    |                         flight :(  | containing “flight” and with a negative attitude.   |
    +------------------------------------+-----------------------------------------------------+
    |                          traffic ? | containing “traffic” and asking a question.         |
    +------------------------------------+-----------------------------------------------------+

    https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
    """  # noqa: E501
    pass


@make_dataframe
@authenticate
def search_users(q, page=None, count=None, include_entities=None):
    """
    Provides a simple, relevance-based search interface to public user
        accounts on Twitter.

    :param q: (str - required) The search query to run against people search.
    :param page: (int - optional) Specifies the page of results to retrieve.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param include_entities: (bool - optional) The entities node will not be
        included in embedded Tweet objects when set to False .

    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-users-search
    """
    pass


@make_dataframe
@authenticate
def show_lists(user_id=None, screen_name=None, reverse=None):
    """
    Returns all lists the authenticating or specified user subscribes to,
        including their own.

    :param user_id: (int - optional) The ID of the user for whom to return
        results. Helpful for disambiguating when a valid user ID is also a valid screen
        name. Note: : Specifies the ID of the user to get lists from. Helpful for
        disambiguating when a valid user ID is also a valid screen name.
    :param screen_name: (str - optional) The screen name of the user for whom
        to return results. Helpful for disambiguating when a valid screen name is also
        a user ID.
    :param reverse: (bool - optional) Set this to true if you would like owned
        lists to be returned first. See description above for information on how this
        parameter works.

    https://developer.twitter.com/en/docs/accounts-and-users/create-manage-lists/api-reference/get-lists-list
    """
    pass


@make_dataframe
@authenticate
def show_owned_lists(user_id=None, screen_name=None, count=None, cursor=None):
    """
    Returns the lists owned by the specified Twitter user.

    :param user_id: (int - optional) The ID of the user for whom to return
        results. Helpful for disambiguating when a valid user ID is also a valid screen
        name.
    :param screen_name: (str - optional) The screen name of the user for whom
        to return results. Helpful for disambiguating when a valid screen name is also
        a user ID.
    :param count: (int - optional) Specifies the number of results to retrieve.
    :param cursor: (cursor - optional) Breaks the results into pages. Provide a
        value of -1 to begin paging. Provide values as returned in the response body’s
        next_cursor and previous_cursor attributes to page back and forth in the list.
        It is recommended to always use cursors when the method supports them. See
        Cursoring for more information.

    https://developer.twitter.com/en/docs/accounts-and-users/create-manage-lists/api-reference/get-lists-ownerships
    """
    pass


FUNCTIONS = [
    get_application_rate_limit_status,
    get_available_trends,
    get_favorites,
    get_followers_ids,
    get_followers_list,
    get_friends_ids,
    get_friends_list,
    get_home_timeline,
    get_list_members,
    get_list_memberships,
    get_list_statuses,
    get_list_subscribers,
    get_list_subscriptions,
    get_mentions_timeline,
    get_place_trends,
    get_retweeters_ids,
    get_retweets,
    get_supported_languages,
    get_user_timeline,
    lookup_status,
    lookup_user,
    retweeted_of_me,
    search,
    search_users,
    show_lists,
    show_owned_lists,
]


def set_auth_params(
    app_key=None,
    app_secret=None,
    oauth_token=None,
    oauth_token_secret=None,
    access_token=None,
    token_type="bearer",
    oauth_version=1,
    api_version="1.1",
    client_args=None,
    auth_endpoint="authenticate",
):
    """The main function for authentication.
    Needs to be called once in a session.

    First you need to create a developer account and app:
    https://developer.twitter.com/ to get your credentials.

    Different ways to authenticate:
    https://twython.readthedocs.io/en/latest/usage/starting_out.html
    """
    params = locals()
    for func in FUNCTIONS:
        func.set_auth_params(**params)
    return None


logging.getLogger().setLevel("INFO")
