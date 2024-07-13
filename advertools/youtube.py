"""
.. _youtube:

YouTube Data API
================
"""

from ._yt_helpers import _combine_requests

__all__ = [
    "activities_list",
    "captions_list",
    "channel_sections_list",
    "channels_list",
    "comment_threads_list",
    "comments_list",
    "guide_categories_list",
    "i18n_languages_list",
    "i18n_regions_list",
    "playlist_items_list",
    "playlists_list",
    "search",
    "subscriptions_list",
    "video_categories_list",
    "videos_list",
]


def activities_list(
    key,
    part,
    channelId=None,
    home=None,
    mine=None,
    maxResults=None,
    pageToken=None,
    publishedAfter=None,
    publishedBefore=None,
    regionCode=None,
):
    """Returns a list of channel activity events that match the request
    criteria. For example, you can retrieve events associated with a particular
    channel or with the user's own channel.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies a comma-separated list of
        one or more activity resource properties that the API response will
        include.If the parameter identifies a property that contains child
        properties, the child properties will be included in the response. For
        example, in an activity resource, the snippet property contains other
        properties that identify the type of activity, a display title for the
        activity, and so forth. If you set part=snippet, the API response will
        also contain all of those nested properties.The following list contains
        the part names that you can include in the parameter value and the
        quota cost for each part: contentDetails: 2 id: 0 snippet: 2

    *Filters (specify exactly one of the following parameters):*

    :param channelId: string  The channelId parameter specifies a unique
        YouTube channel ID. The API will then return a list of that channel's
        activities.
    :param home: boolean  Note: This parameter has been deprecated.For requests
        that set this parameter, the API response contains items similar to
        those that a logged-out user would see on the YouTube home page. Note
        that this parameter can only be used in a properly authorized request.
    :param mine: boolean  This parameter can only be used in a properly
        authorized request. Set this parameter's value to true to retrieve a
        feed of the authenticated user's activities.

    *Optional parameters:*

    :param maxResults: unsigned integer  The maxResults parameter specifies the
        maximum number of items that should be returned in the result set.
    :param pageToken: string  The pageToken parameter identifies a specific
        page in the result set that should be returned. In an API response, the
        nextPageToken and prevPageToken properties identify other pages that
        could be retrieved.
    :param publishedAfter: datetime  The publishedAfter parameter specifies the
        earliest date and time that an activity could have occurred for that
        activity to be included in the API response. If the parameter value
        specifies a day, but not a time, then any activities that occurred that
        day will be included in the result set. The value is specified in ISO
        8601 (YYYY-MM-DDThh:mm:ss.sZ) format.
    :param publishedBefore: datetime  The publishedBefore parameter specifies
        the date and time before which an activity must have occurred for that
        activity to be included in the API response. If the parameter value
        specifies a day, but not a time, then any activities that occurred that
        day will be excluded from the result set. The value is specified in ISO
        8601 (YYYY-MM-DDThh:mm:ss.sZ) format.
    :param regionCode: string  The regionCode parameter instructs the API to
        return results for the specified country. The parameter value is an ISO
        3166-1 alpha-2 country code. YouTube uses this value when the
        authorized user's previous activity on YouTube does not provide enough
        information to generate the activity feed.
    """
    args = locals()
    part_params = {"contentDetails", "id", "snippet"}
    if not set(part.split(",")).issubset(part_params):
        raise ValueError(
            "make sure your `part` parameter is one or more of " + str(part_params)
        )
    if sum([bool(p) for p in [channelId, home, mine]]) != 1:
        raise ValueError(
            "make sure you specify exactly one of ['channelId', 'home', 'mine']"
        )

    base_url = "https://www.googleapis.com/youtube/v3/activities"
    return _combine_requests(args, base_url, count=maxResults, max_allowed=50)


def videos_list(
    key,
    part,
    chart=None,
    id=None,
    myRating=None,
    hl=None,
    maxHeight=None,
    maxResults=None,
    maxWidth=None,
    onBehalfOfContentOwner=None,
    pageToken=None,
    regionCode=None,
    videoCategoryId=None,
):
    """Returns a list of videos that match the API request parameters.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies a comma-separated list of
        one or more video resource properties that the API response will
        include.If the parameter identifies a property that contains child
        properties, the child properties will be included in the response. For
        example, in a video resource, the snippet property contains the
        channelId, title, description, tags, and categoryId properties. As
        such, if you set part=snippet, the API response will contain all of
        those properties.The following list contains the part names that you
        can include in the parameter value and the quota cost for each part:
        contentDetails: 2 fileDetails: 1 id: 0 liveStreamingDetails: 2
        localizations: 2 player: 0 processingDetails: 1 recordingDetails: 2
        snippet: 2 statistics: 2 status: 2 suggestions: 1 topicDetails: 2

    *Filters (specify exactly one of the following parameters):*

    :param chart: string  The chart parameter identifies the chart that you
        want to retrieve.Acceptable values are: mostPopular – Return the most
        popular videos for the specified content region and video category.
    :param id: string  The id parameter specifies a comma-separated list of the
        YouTube video ID(s) for the resource(s) that are being retrieved. In a
        video resource, the id property specifies the video's ID.
    :param myRating: string  This parameter can only be used in a properly
        authorized request. Set this parameter's value to like or dislike to
        instruct the API to only return videos liked or disliked by the
        authenticated user.Acceptable values are: dislike – Returns only videos
        disliked by the authenticated user. like – Returns only video liked by
        the authenticated user.

    *Optional parameters:*

    :param hl: string  The hl parameter instructs the API to retrieve localized
        resource metadata for a specific application language that the YouTube
        website supports. The parameter value must be a language code included
        in the list returned by the i18nLanguages.list method.If localized
        resource details are available in that language, the resource's
        snippet.localized object will contain the localized values. However, if
        localized details are not available, the snippet.localized object will
        contain resource details in the resource's default language.
    :param maxHeight: unsigned integer  The maxHeight parameter specifies the
        maximum height of the embedded player returned in the player.embedHtml
        property. You can use this parameter to specify that instead of the
        default dimensions, the embed code should use a height appropriate for
        your application layout. If the maxWidth parameter is also provided,
        the player may be shorter than the maxHeight in order to not violate
        the maximum width. Acceptable values are 72 to 8192, inclusive.
    :param maxResults: unsigned integer  The maxResults parameter specifies the
        maximum number of items that should be returned in the result set.
    :param maxWidth: unsigned integer  The maxWidth parameter specifies the
        maximum width of the embedded player returned in the player.embedHtml
        property. You can use this parameter to specify that instead of the
        default dimensions, the embed code should use a width appropriate for
        your application layout.If the maxHeight parameter is also provided,
        the player may be narrower than maxWidth in order to not violate the
        maximum height. Acceptable values are 72 to 8192, inclusive.
    :param onBehalfOfContentOwner: string  This parameter can only be used in a
        properly authorized request. Note: This parameter is intended
        exclusively for YouTube content partners.The onBehalfOfContentOwner
        parameter indicates that the request's authorization credentials
        identify a YouTube CMS user who is acting on behalf of the content
        owner specified in the parameter value. This parameter is intended for
        YouTube content partners that own and manage many different YouTube
        channels. It allows content owners to authenticate once and get access
        to all their video and channel data, without having to provide
        authentication credentials for each individual channel. The CMS account
        that the user authenticates with must be linked to the specified
        YouTube content owner.
    :param pageToken: string  The pageToken parameter identifies a specific
        page in the result set that should be returned. In an API response, the
        nextPageToken and prevPageToken properties identify other pages that
        could be retrieved.Note: This parameter is supported for use in
        conjunction with the myRating parameter, but it is not supported for
        use in conjunction with the id parameter.
    :param regionCode: string  The regionCode parameter instructs the API to
        select a video chart available in the specified region. This parameter
        can only be used in conjunction with the chart parameter. The parameter
        value is an ISO 3166-1 alpha-2 country code.
    :param videoCategoryId: string  The videoCategoryId parameter identifies
        the video category for which the chart should be retrieved. This
        parameter can only be used in conjunction with the chart parameter. By
        default, charts are not restricted to a particular category. The
        default value is 0.
    """
    args = locals()
    part_params = {
        "contentDetails",
        "id",
        "processingDetails",
        "fileDetails",
        "snippet",
        "localizations",
        "suggestions",
        "statistics",
        "liveStreamingDetails",
        "player",
        "status",
        "recordingDetails",
        "topicDetails",
    }
    if not set(part.split(",")).issubset(part_params):
        raise ValueError(
            "make sure your `part` parameter is one or more of " + str(part_params)
        )
    if sum([bool(p) for p in [chart, id, myRating]]) != 1:
        raise ValueError(
            "make sure you specify exactly one of ['chart', 'id', 'myRating']"
        )

    base_url = "https://www.googleapis.com/youtube/v3/videos"
    return _combine_requests(args, base_url, count=maxResults, max_allowed=50)


def video_categories_list(key, part, id=None, regionCode=None, hl=None):
    """Returns a list of categories that can be associated with YouTube videos.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies the videoCategory
        resource properties that the API response will include. Set the
        parameter value to snippet. The snippet part has a quota cost of 2
        units.

    *Filters (specify exactly one of the following parameters):*

    :param id: string  The id parameter specifies a comma-separated list of
        video category IDs for the resources that you are retrieving.
    :param regionCode: string  The regionCode parameter instructs the API to
        return the list of video categories available in the specified country.
        The parameter value is an ISO 3166-1 alpha-2 country code.

    *Optional parameters:*

    :param hl: string  The hl parameter specifies the language that should be
        used for text values in the API response. The default value is en_US.
    """
    args = locals()
    if sum([bool(p) for p in [id, regionCode]]) != 1:
        raise ValueError("make sure you specify exactly one of ['id', 'regionCode']")

    base_url = "https://www.googleapis.com/youtube/v3/videoCategories"
    return _combine_requests(args, base_url, count=None, max_allowed=None)


def search(
    key,
    part,
    forContentOwner=None,
    forDeveloper=None,
    forMine=None,
    relatedToVideoId=None,
    channelId=None,
    channelType=None,
    eventType=None,
    location=None,
    locationRadius=None,
    maxResults=None,
    onBehalfOfContentOwner=None,
    order=None,
    pageToken=None,
    publishedAfter=None,
    publishedBefore=None,
    q=None,
    regionCode=None,
    relevanceLanguage=None,
    safeSearch=None,
    topicId=None,
    type=None,
    videoCaption=None,
    videoCategoryId=None,
    videoDefinition=None,
    videoDimension=None,
    videoDuration=None,
    videoEmbeddable=None,
    videoLicense=None,
    videoSyndicated=None,
    videoType=None,
):
    """Returns a collection of search results that match the query parameters
    specified in the API request. By default, a search result set identifies
    matching  video ,  channel , and  playlist  resources, but you can also
    configure queries to only retrieve a specific type of resource.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies a comma-separated list of
        one or more search resource properties that the API response will
        include. Set the parameter value to snippet.

    *Filters (specify 0 or 1 of the following parameters):*

    :param forContentOwner: boolean  This parameter can only be used in a
        properly authorized request, and it is intended exclusively for YouTube
        content partners.The forContentOwner parameter restricts the search to
        only retrieve videos owned by the content owner identified by the
        onBehalfOfContentOwner parameter. If forContentOwner is set to true,
        the request must also meet these requirements:The
        onBehalfOfContentOwner parameter is required.The user authorizing the
        request must be using an account linked to the specified content
        owner.The type parameter value must be set to video.None of the
        following other parameters can be set: videoDefinition, videoDimension,
        videoDuration, videoLicense, videoEmbeddable, videoSyndicated,
        videoType.
    :param forDeveloper: boolean  This parameter can only be used in a properly
        authorized request. The forDeveloper parameter restricts the search to
        only retrieve videos uploaded via the developer's application or
        website. The API server uses the request's authorization credentials to
        identify the developer. The forDeveloper parameter can be used in
        conjunction with optional search parameters like the q parameter.For
        this feature, each uploaded video is automatically tagged with the
        project number that is associated with the developer's application in
        the Google Developers Console.When a search request subsequently sets
        the forDeveloper parameter to true, the API server uses the request's
        authorization credentials to identify the developer. Therefore, a
        developer can restrict results to videos uploaded through the
        developer's own app or website but not to videos uploaded through other
        apps or sites.
    :param forMine: boolean  This parameter can only be used in a properly
        authorized request. The forMine parameter restricts the search to only
        retrieve videos owned by the authenticated user. If you set this
        parameter to true, then the type parameter's value must also be set to
        video. In addition, none of the following other parameters can be set
        in the same request: videoDefinition, videoDimension, videoDuration,
        videoLicense, videoEmbeddable, videoSyndicated, videoType.
    :param relatedToVideoId: string  The relatedToVideoId parameter retrieves a
        list of videos that are related to the video that the parameter value
        identifies. The parameter value must be set to a YouTube video ID and,
        if you are using this parameter, the type parameter must be set to
        video.Note that if the relatedToVideoId parameter is set, the only
        other supported parameters are part, maxResults, pageToken, regionCode,
        relevanceLanguage, safeSearch, type (which must be set to video), and
        fields.

    *Optional parameters:*

    :param channelId: string  The channelId parameter indicates that the API
        response should only contain resources created by the channel. Note:
        Search results are constrained to a maximum of 500 videos if your
        request specifies a value for the channelId parameter and sets the type
        parameter value to video, but it does not also set one of the
        forContentOwner, forDeveloper, or forMine filters.
    :param channelType: string  The channelType parameter lets you restrict a
        search to a particular type of channel.Acceptable values are: any –
        Return all channels. show – Only retrieve shows.
    :param eventType: string  The eventType parameter restricts a search to
        broadcast events. If you specify a value for this parameter, you must
        also set the type parameter's value to video.Acceptable values are:
        completed – Only include completed broadcasts. live – Only include
        active broadcasts. upcoming – Only include upcoming broadcasts.
    :param location: string  The location parameter, in conjunction with the
        locationRadius parameter, defines a circular geographic area and also
        restricts a search to videos that specify, in their metadata, a
        geographic location that falls within that area. The parameter value is
        a string that specifies latitude/longitude coordinates e.g.
        (37.42307,-122.08427).The location parameter value identifies the point
        at the center of the area.The locationRadius parameter specifies the
        maximum distance that the location associated with a video can be from
        that point for the video to still be included in the search results.The
        API returns an error if your request specifies a value for the location
        parameter but does not also specify a value for the locationRadius
        parameter.
    :param locationRadius: string  The locationRadius parameter, in conjunction
        with the location parameter, defines a circular geographic area.The
        parameter value must be a floating point number followed by a
        measurement unit. Valid measurement units are m, km, ft, and mi. For
        example, valid parameter values include 1500m, 5km, 10000ft, and
        0.75mi. The API does not support locationRadius parameter values larger
        than 1000 kilometers.Note: See the definition of the location parameter
        for more information.
    :param maxResults: unsigned integer  The maxResults parameter specifies the
        maximum number of items that should be returned in the result set.
    :param onBehalfOfContentOwner: string  This parameter can only be used in a
        properly authorized request. Note: This parameter is intended
        exclusively for YouTube content partners.The onBehalfOfContentOwner
        parameter indicates that the request's authorization credentials
        identify a YouTube CMS user who is acting on behalf of the content
        owner specified in the parameter value. This parameter is intended for
        YouTube content partners that own and manage many different YouTube
        channels. It allows content owners to authenticate once and get access
        to all their video and channel data, without having to provide
        authentication credentials for each individual channel. The CMS account
        that the user authenticates with must be linked to the specified
        YouTube content owner.
    :param order: string  The order parameter specifies the method that will be
        used to order resources in the API response. The default value is
        relevance.Acceptable values are: date – Resources are sorted in reverse
        chronological order based on the date they were created. rating –
        Resources are sorted from highest to lowest rating. relevance –
        Resources are sorted based on their relevance to the search query. This
        is the default value for this parameter. title – Resources are sorted
        alphabetically by title. videoCount – Channels are sorted in descending
        order of their number of uploaded videos. viewCount – Resources are
        sorted from highest to lowest number of views. For live broadcasts,
        videos are sorted by number of concurrent viewers while the broadcasts
        are ongoing.
    :param pageToken: string  The pageToken parameter identifies a specific
        page in the result set that should be returned. In an API response, the
        nextPageToken and prevPageToken properties identify other pages that
        could be retrieved.
    :param publishedAfter: datetime  The publishedAfter parameter indicates
        that the API response should only contain resources created at or after
        the specified time. The value is an RFC 3339 formatted date-time value
        (1970-01-01T00:00:00Z).
    :param publishedBefore: datetime  The publishedBefore parameter indicates
        that the API response should only contain resources created before or
        at the specified time. The value is an RFC 3339 formatted date-time
        value (1970-01-01T00:00:00Z).
    :param q: string  The q parameter specifies the query term to search
        for.Your request can also use the Boolean NOT (-) and OR (|) operators
        to exclude videos or to find videos that are associated with one of
        several search terms. For example, to search for videos matching either
        "boating" or "sailing", set the q parameter value to boating|sailing.
        Similarly, to search for videos matching either "boating" or "sailing"
        but not "fishing", set the q parameter value to boating|sailing
        -fishing. Note that the pipe character must be URL-escaped when it is
        sent in your API request. The URL-escaped value for the pipe character
        is %7C.
    :param regionCode: string  The regionCode parameter instructs the API to
        return search results for videos that can be viewed in the specified
        country. The parameter value is an ISO 3166-1 alpha-2 country code.
    :param relevanceLanguage: string  The relevanceLanguage parameter instructs
        the API to return search results that are most relevant to the
        specified language. The parameter value is typically an ISO 639-1 two-
        letter language code. However, you should use the values zh-Hans for
        simplified Chinese and zh-Hant for traditional Chinese. Please note
        that results in other languages will still be returned if they are
        highly relevant to the search query term.
    :param safeSearch: string  The safeSearch parameter indicates whether the
        search results should include restricted content as well as standard
        content.Acceptable values are: moderate – YouTube will filter some
        content from search results and, at the least, will filter content that
        is restricted in your locale. Based on their content, search results
        could be removed from search results or demoted in search results. This
        is the default parameter value. none – YouTube will not filter the
        search result set. strict – YouTube will try to exclude all restricted
        content from the search result set. Based on their content, search
        results could be removed from search results or demoted in search
        results.
    :param topicId: string  The topicId parameter indicates that the API
        response should only contain resources associated with the specified
        topic. The value identifies a Freebase topic ID.Important: Due to the
        deprecation of Freebase and the Freebase API, the topicId parameter
        started working differently as of February 27, 2017. At that time,
        YouTube started supporting a small set of curated topic IDs, and you
        can only use that smaller set of IDs as values for this parameter.  See
        topic IDs supported as of February 15, 2017  Topics  Music topics
        /m/04rlf  Music (parent topic)  /m/02mscn  Christian music  /m/0ggq0m
        Classical music  /m/01lyv  Country  /m/02lkt  Electronic music
        /m/0glt670  Hip hop music  /m/05rwpb  Independent music  /m/03_d0  Jazz
        /m/028sqc  Music of Asia  /m/0g293  Music of Latin America  /m/064t9
        Pop music  /m/06cqb  Reggae  /m/06j6l  Rhythm and blues  /m/06by7  Rock
        music  /m/0gywn  Soul music  Gaming topics  /m/0bzvm2  Gaming (parent
        topic)  /m/025zzc  Action game  /m/02ntfj  Action-adventure game
        /m/0b1vjn  Casual game  /m/02hygl  Music video game  /m/04q1x3q  Puzzle
        video game  /m/01sjng  Racing video game  /m/0403l3g  Role-playing
        video game  /m/021bp2  Simulation video game  /m/022dc6  Sports game
        /m/03hf_rm  Strategy video game  Sports topics  /m/06ntj  Sports
        (parent topic)  /m/0jm\_  American football  /m/018jz  Baseball
        /m/018w8  Basketball  /m/01cgz  Boxing  /m/09xp\_  Cricket  /m/02vx4
        Football  /m/037hz  Golf  /m/03tmr  Ice hockey  /m/01h7lh  Mixed
        martial arts  /m/0410tth  Motorsport  /m/07bs0  Tennis  /m/07_53
        Volleyball  Entertainment topics  /m/02jjt  Entertainment (parent
        topic)  /m/09kqc  Humor  /m/02vxn  Movies  /m/05qjc  Performing arts
        /m/066wd  Professional wrestling  /m/0f2f9  TV shows  Lifestyle topics
        /m/019_rr  Lifestyle (parent topic)  /m/032tl  Fashion  /m/027x7n
        Fitness  /m/02wbm  Food  /m/03glg  Hobby  /m/068hy  Pets  /m/041xxh
        Physical attractiveness [Beauty]  /m/07c1v  Technology  /m/07bxq
        Tourism  /m/07yv9  Vehicles  Society topics  /m/098wr  Society (parent
        topic)  /m/09s1f  Business  /m/0kt51  Health  /m/01h6rj  Military
        /m/05qt0  Politics  /m/06bvp  Religion  Other topics  /m/01k8wb
        Knowledge
    :param type: string  The type parameter restricts a search query to only
        retrieve a particular type of resource. The value is a comma-separated
        list of resource types. The default value is
        video,channel,playlist.Acceptable values are: channelplaylistvideo
    :param videoCaption: string  The videoCaption parameter indicates whether
        the API should filter video search results based on whether they have
        captions. If you specify a value for this parameter, you must also set
        the type parameter's value to video.Acceptable values are: any – Do not
        filter results based on caption availability. closedCaption – Only
        include videos that have captions. none – Only include videos that do
        not have captions.
    :param videoCategoryId: string  The videoCategoryId parameter filters video
        search results based on their category. If you specify a value for this
        parameter, you must also set the type parameter's value to video.
    :param videoDefinition: string  The videoDefinition parameter lets you
        restrict a search to only include either high definition (HD) or
        standard definition (SD) videos. HD videos are available for playback
        in at least 720p, though higher resolutions, like 1080p, might also be
        available. If you specify a value for this parameter, you must also set
        the type parameter's value to video.Acceptable values are: any – Return
        all videos, regardless of their resolution. high – Only retrieve HD
        videos. standard – Only retrieve videos in standard definition.
    :param videoDimension: string  The videoDimension parameter lets you
        restrict a search to only retrieve 2D or 3D videos. If you specify a
        value for this parameter, you must also set the type parameter's value
        to video.Acceptable values are: 2d – Restrict search results to exclude
        3D videos. 3d – Restrict search results to only include 3D videos. any
        – Include both 3D and non-3D videos in returned results. This is the
        default value.
    :param videoDuration: string  The videoDuration parameter filters video
        search results based on their duration. If you specify a value for this
        parameter, you must also set the type parameter's value to
        video.Acceptable values are: any – Do not filter video search results
        based on their duration. This is the default value. long – Only include
        videos longer than 20 minutes. medium – Only include videos that are
        between four and 20 minutes long (inclusive). short – Only include
        videos that are less than four minutes long.
    :param videoEmbeddable: string  The videoEmbeddable parameter lets you to
        restrict a search to only videos that can be embedded into a webpage.
        If you specify a value for this parameter, you must also set the type
        parameter's value to video.Acceptable values are: any – Return all
        videos, embeddable or not. true – Only retrieve embeddable videos.
    :param videoLicense: string  The videoLicense parameter filters search
        results to only include videos with a particular license. YouTube lets
        video uploaders choose to attach either the Creative Commons license or
        the standard YouTube license to each of their videos. If you specify a
        value for this parameter, you must also set the type parameter's value
        to video.Acceptable values are: any – Return all videos, regardless of
        which license they have, that match the query parameters.
        creativeCommon – Only return videos that have a Creative Commons
        license. Users can reuse videos with this license in other videos that
        they create. Learn more. youtube – Only return videos that have the
        standard YouTube license.
    :param videoSyndicated: string  The videoSyndicated parameter lets you to
        restrict a search to only videos that can be played outside
        youtube.com. If you specify a value for this parameter, you must also
        set the type parameter's value to video.Acceptable values are: any –
        Return all videos, syndicated or not. true – Only retrieve syndicated
        videos.
    :param videoType: string  The videoType parameter lets you restrict a
        search to a particular type of videos. If you specify a value for this
        parameter, you must also set the type parameter's value to
        video.Acceptable values are: any – Return all videos. episode – Only
        retrieve episodes of shows. movie – Only retrieve movies.
    """
    args = locals()

    base_url = "https://www.googleapis.com/youtube/v3/search"
    return _combine_requests(args, base_url, count=maxResults, max_allowed=50)


def subscriptions_list(
    key,
    part,
    channelId=None,
    id=None,
    mine=None,
    myRecentSubscribers=None,
    mySubscribers=None,
    forChannelId=None,
    maxResults=None,
    onBehalfOfContentOwner=None,
    onBehalfOfContentOwnerChannel=None,
    order=None,
    pageToken=None,
):
    """Returns subscription resources that match the API request criteria.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies a comma-separated list of
        one or more subscription resource properties that the API response will
        include.If the parameter identifies a property that contains child
        properties, the child properties will be included in the response. For
        example, in a subscription resource, the snippet property contains
        other properties, such as a display title for the subscription. If you
        set part=snippet, the API response will also contain all of those
        nested properties.The following list contains the part names that you
        can include in the parameter value and the quota cost for each part:
        contentDetails: 2 id: 0 snippet: 2 subscriberSnippet: 2

    *Filters (specify exactly one of the following parameters):*

    :param channelId: string  The channelId parameter specifies a YouTube
        channel ID. The API will only return that channel's subscriptions.
    :param id: string  The id parameter specifies a comma-separated list of the
        YouTube subscription ID(s) for the resource(s) that are being
        retrieved. In a subscription resource, the id property specifies the
        YouTube subscription ID.
    :param mine: boolean  This parameter can only be used in a properly
        authorized request. Set this parameter's value to true to retrieve a
        feed of the authenticated user's subscriptions.
    :param myRecentSubscribers: boolean  This parameter can only be used in a
        properly authorized request. Set this parameter's value to true to
        retrieve a feed of the subscribers of the authenticated user in reverse
        chronological order (newest first).Note that this parameter only
        supports retrieval of the most recent 1000 subscribers to the
        authenticated user's channel. To retrieve a complete list of
        subscribers, use the mySubscribers parameter. That parameter, which
        does not return subscribers in a particular order, does not limit the
        number of subscribers that can be retrieved.
    :param mySubscribers: boolean  This parameter can only be used in a
        properly authorized request. Set this parameter's value to true to
        retrieve a feed of the subscribers of the authenticated user in no
        particular order.

    *Optional parameters:*

    :param forChannelId: string  The forChannelId parameter specifies a comma-
        separated list of channel IDs. The API response will then only contain
        subscriptions matching those channels.
    :param maxResults: unsigned integer  The maxResults parameter specifies the
        maximum number of items that should be returned in the result set.
    :param onBehalfOfContentOwner: string  Note: This parameter is intended
        exclusively for YouTube content partners.The onBehalfOfContentOwner
        parameter indicates that the request's authorization credentials
        identify a YouTube CMS user who is acting on behalf of the content
        owner specified in the parameter value. This parameter is intended for
        YouTube content partners that own and manage many different YouTube
        channels. It allows content owners to authenticate once and get access
        to all their video and channel data, without having to provide
        authentication credentials for each individual channel. The CMS account
        that the user authenticates with must be linked to the specified
        YouTube content owner.
    :param onBehalfOfContentOwnerChannel: string  This parameter can only be
        used in a properly authorized request. Note: This parameter is intended
        exclusively for YouTube content partners.The
        onBehalfOfContentOwnerChannel parameter specifies the YouTube channel
        ID of the channel to which a video is being added. This parameter is
        required when a request specifies a value for the
        onBehalfOfContentOwner parameter, and it can only be used in
        conjunction with that parameter. In addition, the request must be
        authorized using a CMS account that is linked to the content owner that
        the onBehalfOfContentOwner parameter specifies. Finally, the channel
        that the onBehalfOfContentOwnerChannel parameter value specifies must
        be linked to the content owner that the onBehalfOfContentOwner
        parameter specifies.This parameter is intended for YouTube content
        partners that own and manage many different YouTube channels. It allows
        content owners to authenticate once and perform actions on behalf of
        the channel specified in the parameter value, without having to provide
        authentication credentials for each separate channel.
    :param order: string  The order parameter specifies the method that will be
        used to sort resources in the API response. The default value is
        SUBSCRIPTION_ORDER_RELEVANCE.Acceptable values are: alphabetical – Sort
        alphabetically. relevance – Sort by relevance. unread – Sort by order
        of activity.
    :param pageToken: string  The pageToken parameter identifies a specific
        page in the result set that should be returned. In an API response, the
        nextPageToken and prevPageToken properties identify other pages that
        could be retrieved.
    """
    args = locals()
    part_params = {"contentDetails", "id", "subscriberSnippet", "snippet"}
    if not set(part.split(",")).issubset(part_params):
        raise ValueError(
            "make sure your `part` parameter is one or more of " + str(part_params)
        )
    if (
        sum(
            [bool(p) for p in [channelId, id, mine, myRecentSubscribers, mySubscribers]]
        )
        != 1
    ):
        raise ValueError(
            """make sure you specify exactly one of
        ['channelId', 'id', 'mine', 'myRecentSubscribers', 'mySubscribers']"""
        )

    base_url = "https://www.googleapis.com/youtube/v3/subscriptions"
    return _combine_requests(args, base_url, count=maxResults, max_allowed=50)


def i18n_regions_list(key, part, hl=None):
    """Returns a list of content regions that the YouTube website supports.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies the i18nRegion resource
        properties that the API response will include. Set the parameter value
        to snippet. The snippet part has a quota cost of 1 unit.

    *Optional parameters:*

    :param hl: string  The hl parameter specifies the language that should be
        used for text values in the API response. The default value is en_US.
    """
    args = locals()

    base_url = "https://www.googleapis.com/youtube/v3/i18nRegions"
    return _combine_requests(args, base_url, count=None, max_allowed=None)


def playlists_list(
    key,
    part,
    channelId=None,
    id=None,
    mine=None,
    hl=None,
    maxResults=None,
    onBehalfOfContentOwner=None,
    onBehalfOfContentOwnerChannel=None,
    pageToken=None,
):
    """Returns a collection of playlists that match the API request parameters.
    For example, you can retrieve all playlists that the authenticated user
    owns, or you can retrieve one or more playlists by their unique IDs.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies a comma-separated list of
        one or more playlist resource properties that the API response will
        include.If the parameter identifies a property that contains child
        properties, the child properties will be included in the response. For
        example, in a playlist resource, the snippet property contains
        properties like author, title, description, tags, and timeCreated. As
        such, if you set part=snippet, the API response will contain all of
        those properties.The following list contains the part names that you
        can include in the parameter value and the quota cost for each part:
        contentDetails: 2 id: 0 localizations: 2 player: 0 snippet: 2 status: 2

    *Filters (specify exactly one of the following parameters):*

    :param channelId: string  This value indicates that the API should only
        return the specified channel's playlists.
    :param id: string  The id parameter specifies a comma-separated list of the
        YouTube playlist ID(s) for the resource(s) that are being retrieved. In
        a playlist resource, the id property specifies the playlist's YouTube
        playlist ID.
    :param mine: boolean  This parameter can only be used in a properly
        authorized request. Set this parameter's value to true to instruct the
        API to only return playlists owned by the authenticated user.

    *Optional parameters:*

    :param hl: string  The hl parameter instructs the API to retrieve localized
        resource metadata for a specific application language that the YouTube
        website supports. The parameter value must be a language code included
        in the list returned by the i18nLanguages.list method.If localized
        resource details are available in that language, the resource's
        snippet.localized object will contain the localized values. However, if
        localized details are not available, the snippet.localized object will
        contain resource details in the resource's default language.
    :param maxResults: unsigned integer  The maxResults parameter specifies the
        maximum number of items that should be returned in the result set.
    :param onBehalfOfContentOwner: string  This parameter can only be used in a
        properly authorized request. Note: This parameter is intended
        exclusively for YouTube content partners.The onBehalfOfContentOwner
        parameter indicates that the request's authorization credentials
        identify a YouTube CMS user who is acting on behalf of the content
        owner specified in the parameter value. This parameter is intended for
        YouTube content partners that own and manage many different YouTube
        channels. It allows content owners to authenticate once and get access
        to all their video and channel data, without having to provide
        authentication credentials for each individual channel. The CMS account
        that the user authenticates with must be linked to the specified
        YouTube content owner.
    :param onBehalfOfContentOwnerChannel: string  This parameter can only be
        used in a properly authorized request. Note: This parameter is intended
        exclusively for YouTube content partners.The
        onBehalfOfContentOwnerChannel parameter specifies the YouTube channel
        ID of the channel to which a video is being added. This parameter is
        required when a request specifies a value for the
        onBehalfOfContentOwner parameter, and it can only be used in
        conjunction with that parameter. In addition, the request must be
        authorized using a CMS account that is linked to the content owner that
        the onBehalfOfContentOwner parameter specifies. Finally, the channel
        that the onBehalfOfContentOwnerChannel parameter value specifies must
        be linked to the content owner that the onBehalfOfContentOwner
        parameter specifies.This parameter is intended for YouTube content
        partners that own and manage many different YouTube channels. It allows
        content owners to authenticate once and perform actions on behalf of
        the channel specified in the parameter value, without having to provide
        authentication credentials for each separate channel.
    :param pageToken: string  The pageToken parameter identifies a specific
        page in the result set that should be returned. In an API response, the
        nextPageToken and prevPageToken properties identify other pages that
        could be retrieved.
    """
    args = locals()
    part_params = {
        "contentDetails",
        "id",
        "snippet",
        "localizations",
        "player",
        "status",
    }
    if not set(part.split(",")).issubset(part_params):
        raise ValueError(
            "make sure your `part` parameter is one or more of " + str(part_params)
        )
    if sum([bool(p) for p in [channelId, id, mine]]) != 1:
        raise ValueError(
            "make sure you specify exactly one of ['channelId', 'id', 'mine']"
        )

    base_url = "https://www.googleapis.com/youtube/v3/playlists"
    return _combine_requests(args, base_url, count=maxResults, max_allowed=50)


def i18n_languages_list(key, part, hl=None):
    """Returns a list of application languages that the YouTube website
    supports.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies the i18nLanguage resource
        properties that the API response will include. Set the parameter value
        to snippet. The snippet part has a quota cost of 1 unit.

    *Optional parameters:*

    :param hl: string  The hl parameter specifies the language that should be
        used for text values in the API response. The default value is en_US.
    """
    args = locals()

    base_url = "https://www.googleapis.com/youtube/v3/i18nLanguages"
    return _combine_requests(args, base_url, count=None, max_allowed=None)


def playlist_items_list(
    key,
    part,
    id=None,
    playlistId=None,
    maxResults=None,
    onBehalfOfContentOwner=None,
    pageToken=None,
    videoId=None,
):
    """Returns a collection of playlist items that match the API request
    parameters. You can retrieve all of the playlist items in a specified
    playlist or retrieve one or more playlist items by their unique IDs.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies a comma-separated list of
        one or more playlistItem resource properties that the API response will
        include.If the parameter identifies a property that contains child
        properties, the child properties will be included in the response. For
        example, in a playlistItem resource, the snippet property contains
        numerous fields, including the title, description, position, and
        resourceId properties. As such, if you set part=snippet, the API
        response will contain all of those properties.The following list
        contains the part names that you can include in the parameter value and
        the quota cost for each part: contentDetails: 2 id: 0 snippet: 2
        status: 2

    *Filters (specify exactly one of the following parameters):*

    :param id: string  The id parameter specifies a comma-separated list of one
        or more unique playlist item IDs.
    :param playlistId: string  The playlistId parameter specifies the unique ID
        of the playlist for which you want to retrieve playlist items. Note
        that even though this is an optional parameter, every request to
        retrieve playlist items must specify a value for either the id
        parameter or the playlistId parameter.

    *Optional parameters:*

    :param maxResults: unsigned integer  The maxResults parameter specifies the
        maximum number of items that should be returned in the result set.
    :param onBehalfOfContentOwner: string  This parameter can only be used in a
        properly authorized request. Note: This parameter is intended
        exclusively for YouTube content partners.The onBehalfOfContentOwner
        parameter indicates that the request's authorization credentials
        identify a YouTube CMS user who is acting on behalf of the content
        owner specified in the parameter value. This parameter is intended for
        YouTube content partners that own and manage many different YouTube
        channels. It allows content owners to authenticate once and get access
        to all their video and channel data, without having to provide
        authentication credentials for each individual channel. The CMS account
        that the user authenticates with must be linked to the specified
        YouTube content owner.
    :param pageToken: string  The pageToken parameter identifies a specific
        page in the result set that should be returned. In an API response, the
        nextPageToken and prevPageToken properties identify other pages that
        could be retrieved.
    :param videoId: string  The videoId parameter specifies that the request
        should return only the playlist items that contain the specified video.
    """
    args = locals()
    part_params = {"contentDetails", "id", "snippet", "status"}
    if not set(part.split(",")).issubset(part_params):
        raise ValueError(
            "make sure your `part` parameter is one or more of " + str(part_params)
        )
    if sum([bool(p) for p in [id, playlistId]]) != 1:
        raise ValueError("make sure you specify exactly one of ['id', 'playlistId']")

    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    return _combine_requests(args, base_url, count=maxResults, max_allowed=50)


def guide_categories_list(key, part, id=None, regionCode=None, hl=None):
    """Returns a list of categories that can be associated with YouTube
    channels.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies the guideCategory
        resource properties that the API response will include. Set the
        parameter value to snippet. The snippet part has a quota cost of 2
        units.

    *Filters (specify exactly one of the following parameters):*

    :param id: string  The id parameter specifies a comma-separated list of the
        YouTube channel category ID(s) for the resource(s) that are being
        retrieved. In a guideCategory resource, the id property specifies the
        YouTube channel category ID.
    :param regionCode: string  The regionCode parameter instructs the API to
        return the list of guide categories available in the specified country.
        The parameter value is an ISO 3166-1 alpha-2 country code.

    *Optional parameters:*

    :param hl: string  The hl parameter specifies the language that will be
        used for text values in the API response. The default value is en-US.
    """
    # args = locals()
    # if sum([bool(p) for p in [id, regionCode]]) != 1:
    #     raise ValueError("make sure you specify exactly one of ['id', 'regionCode']")
    #
    # base_url = 'https://www.googleapis.com/youtube/v3/guideCategories'
    # return _combine_requests(args, base_url, count=None, max_allowed=None)
    raise ValueError("This function has been deprecated as of September 9, 2020")


def comment_threads_list(
    key,
    part,
    allThreadsRelatedToChannelId=None,
    channelId=None,
    id=None,
    videoId=None,
    maxResults=None,
    moderationStatus=None,
    order=None,
    pageToken=None,
    searchTerms=None,
    textFormat=None,
):
    """Returns a list of comment threads that match the API request parameters.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies a comma-separated list of
        one or more commentThread resource properties that the API response
        will include.The following list contains the part names that you can
        include in the parameter value and the quota cost for each part: id: 0
        replies: 2 snippet: 2

    *Filters (specify exactly one of the following parameters):*

    :param allThreadsRelatedToChannelId: string  The
        allThreadsRelatedToChannelId parameter instructs the API to return all
        comment threads associated with the specified channel. The response can
        include comments about the channel or about the channel's videos.
    :param channelId: string  The channelId parameter instructs the API to
        return comment threads containing comments about the specified channel.
        (The response will not include comments left on videos that the channel
        uploaded.)
    :param id: string  The id parameter specifies a comma-separated list of
        comment thread IDs for the resources that should be retrieved.
    :param videoId: string  The videoId parameter instructs the API to return
        comment threads associated with the specified video ID.

    *Optional parameters:*

    :param maxResults: unsigned integer  The maxResults parameter specifies the
        maximum number of items that should be returned in the result set.
    :param moderationStatus: string  This parameter can only be used in a
        properly authorized request. Set this parameter to limit the returned
        comment threads to a particular moderation state.Note: This parameter
        is not supported for use in conjunction with the id parameter. The
        default value is published.Acceptable values are: heldForReview –
        Retrieve comment threads that are awaiting review by a moderator. A
        comment thread can be included in the response if the top-level comment
        or at least one of the replies to that comment are awaiting review.
        likelySpam – Retrieve comment threads classified as likely to be spam.
        A comment thread can be included in the response if the top-level
        comment or at least one of the replies to that comment is considered
        likely to be spam. published – Retrieve threads of published comments.
        This is the default value. A comment thread can be included in the
        response if its top-level comment has been published.
    :param order: string  The order parameter specifies the order in which the
        API response should list comment threads. Valid values are: time -
        Comment threads are ordered by time. This is the default
        behavior.relevance - Comment threads are ordered by relevance.Note:
        This parameter is not supported for use in conjunction with the id
        parameter.
    :param pageToken: string  The pageToken parameter identifies a specific
        page in the result set that should be returned. In an API response, the
        nextPageToken property identifies the next page of the result that can
        be retrieved.Note: This parameter is not supported for use in
        conjunction with the id parameter.
    :param searchTerms: string  The searchTerms parameter instructs the API to
        limit the API response to only contain comments that contain the
        specified search terms.Note: This parameter is not supported for use in
        conjunction with the id parameter.
    :param textFormat: string  Set this parameter's value to html or plainText
        to instruct the API to return the comments left by users in html
        formatted or in plain text. The default value is html.Acceptable values
        are: html – Returns the comments in HTML format. This is the default
        value. plainText – Returns the comments in plain text format.
    """
    args = locals()
    part_params = {"id", "replies", "snippet"}
    if not set(part.split(",")).issubset(part_params):
        raise ValueError(
            "make sure your `part` parameter is one or more of " + str(part_params)
        )
    if (
        sum([bool(p) for p in [allThreadsRelatedToChannelId, channelId, id, videoId]])
        != 1
    ):
        raise ValueError(
            """make sure you specify exactly one of
            ['allThreadsRelatedToChannelId', 'channelId', 'id', 'videoId']"""
        )

    base_url = "https://www.googleapis.com/youtube/v3/commentThreads"
    return _combine_requests(args, base_url, count=maxResults, max_allowed=100)


def comments_list(
    key, part, id=None, parentId=None, maxResults=None, pageToken=None, textFormat=None
):
    """Returns a list of comments that match the API request parameters.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies a comma-separated list of
        one or more comment resource properties that the API response will
        include.The following list contains the part names that you can include
        in the parameter value and the quota cost for each part: id: 0 snippet:
        1

    *Filters (specify exactly one of the following parameters):*

    :param id: string  The id parameter specifies a comma-separated list of
        comment IDs for the resources that are being retrieved. In a comment
        resource, the id property specifies the comment's ID.
    :param parentId: string  The parentId parameter specifies the ID of the
        comment for which replies should be retrieved. Note: YouTube currently
        supports replies only for top-level comments. However, replies to
        replies may be supported in the future.

    *Optional parameters:*

    :param maxResults: unsigned integer  The maxResults parameter specifies the
        maximum number of items that should be returned in the result set.
    :param pageToken: string  The pageToken parameter identifies a specific
        page in the result set that should be returned. In an API response, the
        nextPageToken property identifies the next page of the result that can
        be retrieved.Note: This parameter is not supported for use in
        conjunction with the id parameter.
    :param textFormat: string  This parameter indicates whether the API should
        return comments formatted as HTML or as plain text. The default value
        is html.Acceptable values are: html – Returns the comments in HTML
        format. This is the default value. plainText – Returns the comments in
        plain text format.
    """
    args = locals()
    part_params = {"id", "snippet"}
    if not set(part.split(",")).issubset(part_params):
        raise ValueError(
            "make sure your `part` parameter is one or more of " + str(part_params)
        )
    if sum([bool(p) for p in [id, parentId]]) != 1:
        raise ValueError("make sure you specify exactly one of ['id', 'parentId']")

    base_url = "https://www.googleapis.com/youtube/v3/comments"
    return _combine_requests(args, base_url, count=maxResults, max_allowed=100)


def channel_sections_list(
    key, part, channelId=None, id=None, mine=None, hl=None, onBehalfOfContentOwner=None
):
    """Returns a list of   resources that match the API request criteria.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies a comma-separated list of
        one or more channelSection resource properties that the API response
        will include.If the parameter identifies a property that contains child
        properties, the child properties will be included in the response. For
        example, in a channelSection resource, the snippet property contains
        other properties, such as a display title for the section. If you set
        part=snippet, the API response will also contain all of those nested
        properties.The following list contains the part names that you can
        include in the parameter value and the quota cost for each part:
        contentDetails: 2 id: 0 localizations: 2 snippet: 2 targeting: 2

    *Filters (specify exactly one of the following parameters):*

    :param channelId: string  The channelId parameter specifies a YouTube
        channel ID. If a request specifies a value for this parameter, the API
        will only return the specified channel's sections.
    :param id: string  The id parameter specifies a comma-separated list of IDs
        that uniquely identify the channelSection resources that are being
        retrieved. In a channelSection resource, the id property specifies the
        section's ID.
    :param mine: boolean  This parameter can only be used in a properly
        authorized request. Set this parameter's value to true to retrieve a
        feed of the channel sections associated with the authenticated user's
        YouTube channel.

    *Optional parameters:*

    :param hl: string  The hl parameter instructs the API to retrieve localized
        resource metadata for a specific application language that the YouTube
        website supports. The parameter value must be a language code included
        in the list returned by the i18nLanguages.list method.If localized
        resource details are available in that language, the resource's
        snippet.localized object will contain the localized values. However, if
        localized details are not available, the snippet.localized object will
        contain resource details in the resource's default language.
    :param onBehalfOfContentOwner: string  This parameter can only be used in a
        properly authorized request. Note: This parameter is intended
        exclusively for YouTube content partners.The onBehalfOfContentOwner
        parameter indicates that the request's authorization credentials
        identify a YouTube CMS user who is acting on behalf of the content
        owner specified in the parameter value. This parameter is intended for
        YouTube content partners that own and manage many different YouTube
        channels. It allows content owners to authenticate once and get access
        to all their video and channel data, without having to provide
        authentication credentials for each individual channel. The CMS account
        that the user authenticates with must be linked to the specified
        YouTube content owner.
    """
    args = locals()
    part_params = {"contentDetails", "id", "snippet", "localizations", "targeting"}
    if not set(part.split(",")).issubset(part_params):
        raise ValueError(
            "make sure your `part` parameter is one or more of " + str(part_params)
        )
    if sum([bool(p) for p in [channelId, id, mine]]) != 1:
        raise ValueError(
            "make sure you specify exactly one of ['channelId', 'id', 'mine']"
        )

    base_url = "https://www.googleapis.com/youtube/v3/channelSections"
    return _combine_requests(args, base_url, count=None, max_allowed=None)


def channels_list(
    key,
    part,
    categoryId=None,
    forUsername=None,
    id=None,
    managedByMe=None,
    mine=None,
    mySubscribers=None,
    hl=None,
    maxResults=None,
    onBehalfOfContentOwner=None,
    pageToken=None,
):
    """Returns a collection of zero or more   resources that match the request
    criteria.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies a comma-separated list of
        one or more channel resource properties that the API response will
        include.If the parameter identifies a property that contains child
        properties, the child properties will be included in the response. For
        example, in a channel resource, the contentDetails property contains
        other properties, such as the uploads properties. As such, if you set
        part=contentDetails, the API response will also contain all of those
        nested properties.The following list contains the part names that you
        can include in the parameter value and the quota cost for each part:
        auditDetails: 4 brandingSettings: 2 contentDetails: 2
        contentOwnerDetails: 2 id: 0 invideoPromotion: 2 (deprecated)
        localizations: 2 snippet: 2 statistics: 2 status: 2 topicDetails: 2

    *Filters (specify exactly one of the following parameters):*

    :param categoryId: string  The categoryId parameter specifies a YouTube
        guide category, thereby requesting YouTube channels associated with
        that category.
    :param forUsername: string  The forUsername parameter specifies a YouTube
        username, thereby requesting the channel associated with that username.
    :param id: string  The id parameter specifies a comma-separated list of the
        YouTube channel ID(s) for the resource(s) that are being retrieved. In
        a channel resource, the id property specifies the channel's YouTube
        channel ID.
    :param managedByMe: boolean  This parameter can only be used in a properly
        authorized request. Note: This parameter is intended exclusively for
        YouTube content partners.Set this parameter's value to true to instruct
        the API to only return channels managed by the content owner that the
        onBehalfOfContentOwner parameter specifies. The user must be
        authenticated as a CMS account linked to the specified content owner
        and onBehalfOfContentOwner must be provided.
    :param mine: boolean  This parameter can only be used in a properly
        authorized request. Set this parameter's value to true to instruct the
        API to only return channels owned by the authenticated user.
    :param mySubscribers: boolean  This parameter has been deprecated. This
        parameter can only be used in a properly authorized request. Use the
        subscriptions.list method and its mySubscribers parameter to retrieve a
        list of subscribers to the authenticated user's channel.

    *Optional parameters:*

    :param hl: string  The hl parameter instructs the API to retrieve localized
        resource metadata for a specific application language that the YouTube
        website supports. The parameter value must be a language code included
        in the list returned by the i18nLanguages.list method.If localized
        resource details are available in that language, the resource's
        snippet.localized object will contain the localized values. However, if
        localized details are not available, the snippet.localized object will
        contain resource details in the resource's default language.
    :param maxResults: unsigned integer  The maxResults parameter specifies the
        maximum number of items that should be returned in the result set.
    :param onBehalfOfContentOwner: string  This parameter can only be used in a
        properly authorized request. Note: This parameter is intended
        exclusively for YouTube content partners.The onBehalfOfContentOwner
        parameter indicates that the request's authorization credentials
        identify a YouTube CMS user who is acting on behalf of the content
        owner specified in the parameter value. This parameter is intended for
        YouTube content partners that own and manage many different YouTube
        channels. It allows content owners to authenticate once and get access
        to all their video and channel data, without having to provide
        authentication credentials for each individual channel. The CMS account
        that the user authenticates with must be linked to the specified
        YouTube content owner.
    :param pageToken: string  The pageToken parameter identifies a specific
        page in the result set that should be returned. In an API response, the
        nextPageToken and prevPageToken properties identify other pages that
        could be retrieved.
    """
    args = locals()
    part_params = {
        "contentDetails",
        "id",
        "(deprecated) localizations",
        "snippet",
        "auditDetails",
        "statistics",
        "status",
        "invideoPromotion",
        "brandingSettings",
        "contentOwnerDetails",
        "topicDetails",
    }
    if not set(part.split(",")).issubset(part_params):
        raise ValueError(
            "make sure your `part` parameter is one or more of " + str(part_params)
        )
    if (
        sum(
            [
                bool(p)
                for p in [categoryId, forUsername, id, managedByMe, mine, mySubscribers]
            ]
        )
        != 1
    ):
        raise ValueError(
            """make sure you specify exactly one of
        ['categoryId', 'forUsername', 'id', 'managedByMe', 'mine', 'mySubscribers']"""
        )

    base_url = "https://www.googleapis.com/youtube/v3/channels"
    return _combine_requests(args, base_url, count=maxResults, max_allowed=50)


def captions_list(key, part, videoId, id=None, onBehalfOfContentOwner=None):
    """Returns a list of caption tracks that are associated with a specified
    video. Note that the API response does not contain the actual captions and
    that the  captions.download  method provides the ability to retrieve a
    caption track.

    *Required parameters:*

    :param key: string  Your Google API key.
    :param part: string  The part parameter specifies the caption resource
        parts that the API response will include.The list below contains the
        part names that you can include in the parameter value and the quota
        cost for each part: id: 0 snippet: 1
    :param videoId: string  The videoId parameter specifies the YouTube video
        ID of the video for which the API should return caption tracks.

    *Optional parameters:*

    :param id: string  The id parameter specifies a comma-separated list of IDs
        that identify the caption resources that should be retrieved. Each ID
        must identify a caption track associated with the specified video.
    :param onBehalfOfContentOwner: string  This parameter can only be used in a
        properly authorized request. Note: This parameter is intended
        exclusively for YouTube content partners.The onBehalfOfContentOwner
        parameter indicates that the request's authorization credentials
        identify a YouTube CMS user who is acting on behalf of the content
        owner specified in the parameter value. This parameter is intended for
        YouTube content partners that own and manage many different YouTube
        channels. It allows content owners to authenticate once and get access
        to all their video and channel data, without having to provide
        authentication credentials for each individual channel. The actual CMS
        account that the user authenticates with must be linked to the
        specified YouTube content owner.
    """
    args = locals()
    part_params = {"id", "snippet"}
    if not set(part.split(",")).issubset(part_params):
        raise ValueError(
            "make sure your `part` parameter is one or more of " + str(part_params)
        )

    base_url = "https://www.googleapis.com/youtube/v3/captions"
    return _combine_requests(args, base_url, count=None, max_allowed=None)
