import os

import pytest

import advertools.youtube as yt

youtube_key = os.environ.get('GOOG_CSE_KEY')

skip_api_tests = pytest.mark.skipif(os.environ.get('ADV_TEST_OFFLINE'),
                                    reason='Run all except API dependents')


@skip_api_tests
def test_activities_list():
    result = yt.activities_list(key=youtube_key, part='snippet',
                                channelId='UCv002AUCZaPNwiADqwchijg')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_captions_list():
    result = yt.captions_list(key=youtube_key, part='snippet',
                              videoId='kJQP7kiw5Fk')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_channel_sections_list():
    result = yt.channel_sections_list(key=youtube_key, part='snippet',
                                      channelId='UCv002AUCZaPNwiADqwchijg')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_channels_list():
    result = yt.channels_list(key=youtube_key, part='snippet,statistics',
                              forUsername='youtube')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_comment_threads_list():
    result = yt.comment_threads_list(key=youtube_key,
                                     part='id,replies,snippet',
                                     videoId='PscrVidwxMg')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_comments_list():
    result = yt.comments_list(key=youtube_key, part='snippet',
                              id='UgxKMCc9z4iE7LNW2Hh4AaABAg')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


# @skip_api_tests
# def test_guide_categories_list():
#     result = yt.guide_categories_list(key=youtube_key, part='snippet',
#                                       regionCode='tr', hl='tr')
#     assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_i18n_languages_list():
    result = yt.i18n_languages_list(key=youtube_key, part='snippet')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_i18n_regions_list():
    result = yt.i18n_regions_list(key=youtube_key, part='snippet')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_playlist_items_list():
    result = yt.playlist_items_list(key=youtube_key, part='snippet',
                                    playlistId='PLW0Gy9pTgVntoeYT50HfV144rzuJcrmMg')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_playlists_list():
    result = yt.playlists_list(key=youtube_key, part='snippet',
                               channelId='UCv002AUCZaPNwiADqwchijg')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_search():
    result = yt.search(key=youtube_key, part='snippet', q='test bitcoin')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_subscriptions_list():
    result = yt.subscriptions_list(key=youtube_key, part='snippet',
                                   channelId='UCv002AUCZaPNwiADqwchijg')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_video_categories_list():
    result = yt.video_categories_list(key=youtube_key, part='snippet',
                                      regionCode='de')
    assert {'queryTime', 'param_part'}.issubset(result.columns)


@skip_api_tests
def test_videos_list():
    result = yt.videos_list(key=youtube_key, part='snippet',
                            chart='mostPopular', regionCode='GB', maxResults=9)
    assert {'queryTime', 'param_part'}.issubset(result.columns)

# Test raising errors:


@skip_api_tests
def test_activities_list_raises():
    with pytest.raises(ValueError):
        yt.activities_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.activities_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_captions_list_raises():
    with pytest.raises(ValueError):
        yt.captions_list(key=youtube_key, part='wrong_part', videoId='random')


@skip_api_tests
def test_channel_sections_list_raises():
    with pytest.raises(ValueError):
        yt.channel_sections_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.channel_sections_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_channels_list_raises():
    with pytest.raises(ValueError):
        yt.channels_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.channels_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_comment_threads_list_raises():
    with pytest.raises(ValueError):
        yt.comment_threads_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.comment_threads_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_comments_list_raises():
    with pytest.raises(ValueError):
        yt.comments_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.comments_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_guide_categories_list_raises():
    with pytest.raises(ValueError):
        yt.guide_categories_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.guide_categories_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_playlist_items_list_raises():
    with pytest.raises(ValueError):
        yt.playlist_items_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.playlist_items_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_playlists_list_raises():
    with pytest.raises(ValueError):
        yt.playlists_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.playlists_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_subscriptions_list_raises():
    with pytest.raises(ValueError):
        yt.subscriptions_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.subscriptions_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_video_categories_list_raises():
    with pytest.raises(ValueError):
        yt.video_categories_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.video_categories_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_videos_list_raises():
    with pytest.raises(ValueError):
        yt.videos_list(key=youtube_key, part='wrong_part')

    with pytest.raises(ValueError):
        yt.videos_list(key=youtube_key, part='snippet')


@skip_api_tests
def test_with_zero_results_required():
    result = yt.search(key=youtube_key, part='snippet', q='testing bitcoin',
                       maxResults=0)


@skip_api_tests
def test_empty_list_raises_error():
    with pytest.raises(ValueError):
        yt.search(key=youtube_key, part='snippet', q='testing bitcoin',
                  regionCode=[])


@skip_api_tests
def test_errors_returned_as_df():
    result = yt.search(key='wrong key', part='snippet', q='testing bitcoin')
