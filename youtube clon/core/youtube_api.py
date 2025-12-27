import requests
from django.conf import settings
import random


YOUTUBE_API_KEY = getattr(settings, 'YOUTUBE_API_KEY', None)
YOUTUBE_API_BASE_URL = 'https://www.googleapis.com/youtube/v3'


# Sample video data for when API is not available
SAMPLE_VIDEOS = [
    {
        'id': 'BigBuckBunny',
        'title': 'Big Buck Bunny',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 15200000,
        'category': 'Filmler',
        'duration': '9:56',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/BigBuckBunny.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
        'provider': 'external',
    },
    {
        'id': 'ElephantsDream',
        'title': 'Elephants Dream',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 9800000,
        'category': 'Filmler',
        'duration': '10:53',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/ElephantsDream.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
        'provider': 'external',
    },
    {
        'id': 'Sintel',
        'title': 'Sintel',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 12800000,
        'category': 'Filmler',
        'duration': '14:48',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/Sintel.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
        'provider': 'external',
    },
    {
        'id': 'TearsOfSteel',
        'title': 'Tears of Steel',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 8600000,
        'category': 'Filmler',
        'duration': '12:14',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/TearsOfSteel.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4',
        'provider': 'external',
    },
    {
        'id': 'ForBiggerBlazes',
        'title': 'For Bigger Blazes',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 4200000,
        'category': 'Komedi',
        'duration': '0:15',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/ForBiggerBlazes.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
        'provider': 'external',
    },
    {
        'id': 'ForBiggerFun',
        'title': 'For Bigger Fun',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 3900000,
        'category': 'Komedi',
        'duration': '0:15',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/ForBiggerFun.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
        'provider': 'external',
    },
    {
        'id': 'ForBiggerMeltdowns',
        'title': 'For Bigger Meltdowns',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 3100000,
        'category': 'Komedi',
        'duration': '0:15',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/ForBiggerMeltdowns.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4',
        'provider': 'external',
    },
    {
        'id': 'ForBiggerEscapes',
        'title': 'For Bigger Escapes',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 2800000,
        'category': 'Oyun',
        'duration': '0:15',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/ForBiggerEscapes.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
        'provider': 'external',
    },
    {
        'id': 'ForBiggerJoyrides',
        'title': 'For Bigger Joyrides',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 2600000,
        'category': 'Oyun',
        'duration': '0:15',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/ForBiggerJoyrides.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',
        'provider': 'external',
    },
    {
        'id': 'SubaruOutbackOnStreetAndDirt',
        'title': 'Subaru Outback On Street And Dirt',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 5400000,
        'category': 'Spor',
        'duration': '0:30',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/SubaruOutbackOnStreetAndDirt.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4',
        'provider': 'external',
    },
    {
        'id': 'WeAreGoingOnBullrun',
        'title': 'We Are Going On Bullrun',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 4700000,
        'category': 'Spor',
        'duration': '0:30',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/WeAreGoingOnBullrun.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4',
        'provider': 'external',
    },
    {
        'id': 'WhatCarCanYouGetForAGrand',
        'title': 'What Car Can You Get For A Grand',
        'channel_title': 'GTV Samples',
        'channel_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/',
        'view_count': 6200000,
        'category': 'Haberler',
        'duration': '0:30',
        'thumbnail': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/WhatCarCanYouGetForAGrand.jpg',
        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4',
        'provider': 'external',
    },
]

# Reserved for blocked sample ids.
INVALID_SAMPLE_IDS = set()


def get_sample_videos(query='', category='', max_results=50):
    """Get sample videos, optionally filtered by query or category."""
    videos = SAMPLE_VIDEOS.copy()
    videos = [v for v in videos if v.get('id') not in INVALID_SAMPLE_IDS]

    # Filter by category if provided
    if category and category != 'T?m?':
        videos = [v for v in videos if v.get('category') == category]

    # Filter by search query if provided
    if query:
        query_lower = query.lower()
        videos = [
            v for v in videos
            if query_lower in v['title'].lower() or query_lower in v['channel_title'].lower()
        ]

    # Shuffle to mix up the order
    random.shuffle(videos)

    # Add required fields for display
    result = []
    for video in videos[:max_results]:
        youtube_url = video.get('youtube_url')
        video_url = video.get('video_url')
        channel_url = video.get('channel_url')
        provider = video.get('provider', 'youtube')
        source_url = video.get('source_url') or video_url or youtube_url
        thumbnail = video.get('thumbnail') or f"https://img.youtube.com/vi/{video['id']}/maxresdefault.jpg"
        view_count = video.get('view_count', 0)

        result.append({
            'id': video['id'],
            'title': video['title'],
            'description': f"Watch {video['title']} on VideoTube",
            'thumbnail': thumbnail,
            'channel_title': video.get('channel_title', 'Unknown'),
            'channel_id': video.get('channel_id', ''),
            'channel_url': channel_url,
            'published_at': '2024-01-15T12:00:00Z',
            'view_count': view_count,
            'like_count': int(view_count * 0.04),
            'youtube_url': youtube_url,
            'video_url': video_url,
            'source_url': source_url,
            'provider': provider,
            'duration': video.get('duration', '0:00'),
            'category': video.get('category', 'T?m?'),
        })

    return result


def search_youtube_videos(query='', max_results=50, category=''):
    """
    Search YouTube videos using the Data API v3.
    If no API key, returns sample videos.
    """
    # Always return sample videos if no API key
    if not YOUTUBE_API_KEY:
        return get_sample_videos(query=query, category=category, max_results=max_results)

    try:
        if query:
            # Search for videos matching query
            url = f'{YOUTUBE_API_BASE_URL}/search'
            params = {
                'key': YOUTUBE_API_KEY,
                'q': query,
                'part': 'snippet',
                'type': 'video',
                'maxResults': max_results,
                'order': 'relevance',
            }
        else:
            # Get popular videos
            url = f'{YOUTUBE_API_BASE_URL}/videos'
            params = {
                'key': YOUTUBE_API_KEY,
                'part': 'snippet,statistics,status',
                'chart': 'mostPopular',
                'regionCode': 'TR',
                'maxResults': max_results,
            }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        videos = []
        items = data.get('items', [])

        # If search results, we need to get video details for view counts
        if query and items:
            video_ids = [item['id']['videoId'] for item in items if 'videoId' in item.get('id', {})]
            if video_ids:
                details_url = f'{YOUTUBE_API_BASE_URL}/videos'
                details_params = {
                    'key': YOUTUBE_API_KEY,
                    'part': 'snippet,statistics,status',
                    'id': ','.join(video_ids),
                }
                details_response = requests.get(details_url, params=details_params, timeout=10)
                details_response.raise_for_status()
                items = details_response.json().get('items', [])

        for item in items:
            video_id = item['id'] if isinstance(item['id'], str) else item['id'].get('videoId', '')
            snippet = item.get('snippet', {})
            statistics = item.get('statistics', {})

            embeddable = item.get('status', {}).get('embeddable', True)
            if embeddable is False:
                continue

            # Get thumbnail - prefer high quality
            thumbnails = snippet.get('thumbnails', {})
            thumbnail_url = (
                thumbnails.get('maxres', {}).get('url') or
                thumbnails.get('high', {}).get('url') or
                thumbnails.get('medium', {}).get('url') or
                thumbnails.get('default', {}).get('url', '')
            )

            channel_id = snippet.get('channelId', '')
            youtube_url = f'https://www.youtube.com/watch?v={video_id}'

            videos.append({
                'id': video_id,
                'title': snippet.get('title', 'Untitled'),
                'description': snippet.get('description', ''),
                'thumbnail': thumbnail_url,
                'channel_title': snippet.get('channelTitle', 'Unknown'),
                'channel_id': channel_id,
                'channel_url': f"https://www.youtube.com/channel/{channel_id}",
                'published_at': snippet.get('publishedAt', ''),
                'view_count': int(statistics.get('viewCount', 0)),
                'like_count': int(statistics.get('likeCount', 0)),
                'youtube_url': youtube_url,
                'source_url': youtube_url,
                'provider': 'youtube',
            })

        return videos

    except requests.RequestException as e:
        print(f"YouTube API error: {e}")
        return get_sample_videos(query=query, category=category, max_results=max_results)
    except (KeyError, ValueError) as e:
        print(f"Error parsing YouTube response: {e}")
        return get_sample_videos(query=query, category=category, max_results=max_results)


def get_video_details(video_id):
    """Get detailed information about a specific YouTube video."""
    if not YOUTUBE_API_KEY:
        if video_id in INVALID_SAMPLE_IDS:
            return None
        # Return from sample videos if available
        for video in SAMPLE_VIDEOS:
            if video['id'] == video_id:
                youtube_url = video.get('youtube_url')
                video_url = video.get('video_url')
                channel_url = video.get('channel_url')
                provider = video.get('provider', 'youtube')
                source_url = video.get('source_url') or video_url or youtube_url
                thumbnail = video.get('thumbnail') or f"https://img.youtube.com/vi/{video['id']}/maxresdefault.jpg"
                view_count = video.get('view_count', 0)

                return {
                    'id': video['id'],
                    'title': video['title'],
                    'description': f"Watch {video['title']} on VideoTube",
                    'thumbnail': thumbnail,
                    'channel_title': video.get('channel_title', 'Unknown'),
                    'channel_id': video.get('channel_id', ''),
                    'channel_url': channel_url,
                    'published_at': '2024-01-15T12:00:00Z',
                    'view_count': view_count,
                    'like_count': int(view_count * 0.04),
                    'comment_count': int(view_count * 0.001),
                    'duration': video.get('duration', 'PT0M0S'),
                    'youtube_url': youtube_url,
                    'video_url': video_url,
                    'source_url': source_url,
                    'provider': provider,
                }
        return None

    try:
        url = f'{YOUTUBE_API_BASE_URL}/videos'
        params = {
            'key': YOUTUBE_API_KEY,
            'part': 'snippet,statistics,contentDetails,status',
            'id': video_id,
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = data.get('items', [])
        if not items:
            return None

        item = items[0]
        if item.get('status', {}).get('embeddable') is False:
            return None
        snippet = item.get('snippet', {})
        statistics = item.get('statistics', {})
        content_details = item.get('contentDetails', {})

        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = (
            thumbnails.get('maxres', {}).get('url') or
            thumbnails.get('high', {}).get('url') or
            thumbnails.get('medium', {}).get('url', '')
        )

        channel_id = snippet.get('channelId', '')
        youtube_url = f'https://www.youtube.com/watch?v={video_id}'

        return {
            'id': video_id,
            'title': snippet.get('title', 'Untitled'),
            'description': snippet.get('description', ''),
            'thumbnail': thumbnail_url,
            'channel_title': snippet.get('channelTitle', 'Unknown'),
            'channel_id': channel_id,
            'channel_url': f"https://www.youtube.com/channel/{channel_id}",
            'published_at': snippet.get('publishedAt', ''),
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'duration': content_details.get('duration', 'PT0M0S'),
            'youtube_url': youtube_url,
            'source_url': youtube_url,
            'provider': 'youtube',
        }

    except requests.RequestException as e:
        print(f"YouTube API error: {e}")
        return None


def format_view_count(count):
    """
    Format view count like YouTube does (e.g., 1.5M, 234K).
    """
    if count >= 1_000_000_000:
        return f"{count / 1_000_000_000:.1f}B"
    elif count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)


def format_duration(duration_str):
    """
    Convert ISO 8601 duration (PT1H2M3S) to human readable (1:02:03).
    """
    import re
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return "0:00"
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"
