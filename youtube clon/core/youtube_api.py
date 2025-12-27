import requests
from django.conf import settings
import random


YOUTUBE_API_KEY = getattr(settings, 'YOUTUBE_API_KEY', None)
YOUTUBE_API_BASE_URL = 'https://www.googleapis.com/youtube/v3'


# Sample video data for when API is not available
SAMPLE_VIDEOS = [
    # Music
    {'id': 'dQw4w9WgXcQ', 'title': 'Rick Astley - Never Gonna Give You Up', 'channel_title': 'Rick Astley', 'channel_id': 'UCuAXFkgsw1L7xaCfnd5JJOw', 'view_count': 1500000000, 'category': 'Müzik', 'duration': '3:33'},
    {'id': 'JGwWNGJdvx8', 'title': 'Ed Sheeran - Shape of You', 'channel_title': 'Ed Sheeran', 'channel_id': 'UC0C-w0YjGpqDXGB8IHb662A', 'view_count': 6000000000, 'category': 'Müzik', 'duration': '4:24'},
    {'id': 'kJQP7kiw5Fk', 'title': 'Luis Fonsi - Despacito ft. Daddy Yankee', 'channel_title': 'Luis Fonsi', 'channel_id': 'UCLp8RBhQHu9wSsq62j_Ia0g', 'view_count': 8200000000, 'category': 'Müzik', 'duration': '4:42'},
    {'id': 'RgKAFK5djSk', 'title': 'Wiz Khalifa - See You Again ft. Charlie Puth', 'channel_title': 'Wiz Khalifa', 'channel_id': 'UC3lBXcrKFnFAFkfVk5WuKcQ', 'view_count': 5900000000, 'category': 'Müzik', 'duration': '3:57'},
    {'id': '09R8_2nJtjg', 'title': 'Maroon 5 - Sugar', 'channel_title': 'Maroon 5', 'channel_id': 'UCBVjMGOIkavEAhyqpxJ73Dw', 'view_count': 3800000000, 'category': 'Müzik', 'duration': '5:01'},
    {'id': 'YQHsXMglC9A', 'title': 'Adele - Hello', 'channel_title': 'Adele', 'channel_id': 'UCsRM0YB_dabtEPGPTKo-gcw', 'view_count': 3100000000, 'category': 'Müzik', 'duration': '6:07'},
    {'id': 'CevxZvSJLk8', 'title': 'Katy Perry - Roar', 'channel_title': 'Katy Perry', 'channel_id': 'UCYvmuw-JtVrTZQ-7Y4kd63Q', 'view_count': 3700000000, 'category': 'Müzik', 'duration': '4:30'},
    {'id': 'fRh_vgS2dFE', 'title': 'Justin Bieber - Sorry', 'channel_title': 'Justin Bieber', 'channel_id': 'UCHkj014U2CQ2Nv0UZeYpE_A', 'view_count': 3500000000, 'category': 'Müzik', 'duration': '3:26'},
    {'id': 'OPf0YbXqDm0', 'title': 'Mark Ronson - Uptown Funk ft. Bruno Mars', 'channel_title': 'Mark Ronson', 'channel_id': 'UCnycQK-_E7W2yyNcDk8_8WA', 'view_count': 4900000000, 'category': 'Müzik', 'duration': '4:31'},
    {'id': 'pRpeEdMmmQ0', 'title': 'Shakira - Waka Waka', 'channel_title': 'Shakira', 'channel_id': 'UCGnjeahCJW1AF34HBmQTJ-Q', 'view_count': 3400000000, 'category': 'Müzik', 'duration': '3:31'},
    
    # Gaming
    {'id': 'M7lc1UVf-VE', 'title': 'Minecraft: Best Building Tips & Tricks', 'channel_title': 'Dream', 'channel_id': 'UCTkXRDQl0luXxVQrRQvWS6w', 'view_count': 45000000, 'category': 'Oyun', 'duration': '15:42'},
    {'id': 'dMjQ3hA9mEA', 'title': 'Fortnite Chapter 5 - Epic Victory Royale', 'channel_title': 'Ninja', 'channel_id': 'UCAW-NpUFkMyCNrvRSSGIvDQ', 'view_count': 32000000, 'category': 'Oyun', 'duration': '22:18'},
    {'id': 'r2wyWPBRfxY', 'title': 'GTA 6 Trailer Breakdown - Everything You Missed', 'channel_title': 'MrBossForTheWin', 'channel_id': 'UCvmh2tMYzT6P7vWm8w-8b2g', 'view_count': 28000000, 'category': 'Oyun', 'duration': '18:55'},
    {'id': 'qIcTM8WXFjk', 'title': 'Call of Duty: Warzone - Pro Tips', 'channel_title': 'NICKMERCS', 'channel_id': 'UCnbLmH4N-fJvwc2NhhcNJaQ', 'view_count': 15000000, 'category': 'Oyun', 'duration': '25:30'},
    {'id': '2VBcS3opG_8', 'title': 'Valorant Ranked Gameplay - From Iron to Radiant', 'channel_title': 'TenZ', 'channel_id': 'UCsHMOo2dM8s_IFhxgHpSefQ', 'view_count': 12000000, 'category': 'Oyun', 'duration': '32:15'},
    {'id': 'KpKqvC6cXHo', 'title': 'League of Legends - Best Plays 2024', 'channel_title': 'Faker', 'channel_id': 'UCZhmcv9q8IMrfMVmN3k2gNw', 'view_count': 25000000, 'category': 'Oyun', 'duration': '12:45'},
    {'id': 'QH2-TGUlwu4', 'title': 'Elden Ring - Boss Fight Guide', 'channel_title': 'VaatiVidya', 'channel_id': 'UCe0DNp0mKMqrYVaTundyr9w', 'view_count': 18000000, 'category': 'Oyun', 'duration': '28:33'},
    {'id': 'HdKwNHM_fns', 'title': 'Pokemon Scarlet & Violet - Full Walkthrough', 'channel_title': 'Austin John Plays', 'channel_id': 'UCG4PoAtmXf3K6ZbdHQZ5ang', 'view_count': 8500000, 'category': 'Oyun', 'duration': '45:20'},
    
    # Live/Trending
    {'id': '5qap5aO4i9A', 'title': 'Lofi Hip Hop Radio - Beats to Study/Relax', 'channel_title': 'Lofi Girl', 'channel_id': 'UCSJ4gkVC6NrvII8umztf0Ow', 'view_count': 950000000, 'category': 'Canlı', 'duration': 'LIVE'},
    {'id': 'jfKfPfyJRdk', 'title': 'lofi hip hop radio - beats to sleep/chill to', 'channel_title': 'Lofi Girl', 'channel_id': 'UCSJ4gkVC6NrvII8umztf0Ow', 'view_count': 420000000, 'category': 'Canlı', 'duration': 'LIVE'},
    {'id': 'DWcJFNfaw9c', 'title': 'NASA Live: Earth From Space', 'channel_title': 'NASA', 'channel_id': 'UCLA_DiR1FfKNvjuUpBHmylQ', 'view_count': 85000000, 'category': 'Canlı', 'duration': 'LIVE'},
    {'id': 'QlPbtKp0_6s', 'title': 'World News Live 24/7', 'channel_title': 'Sky News', 'channel_id': 'UCoMdktPbSTixAyNGwb-UYkQ', 'view_count': 32000000, 'category': 'Canlı', 'duration': 'LIVE'},
    
    # News
    {'id': 'Y4MnpzG5Sqc', 'title': 'Breaking: Latest World News Update', 'channel_title': 'BBC News', 'channel_id': 'UC16niRr50-MSBwiO3YDb3RA', 'view_count': 5200000, 'category': 'Haberler', 'duration': '8:45'},
    {'id': 'VzhB0a8p0lU', 'title': 'Tech News: AI Revolution 2024', 'channel_title': 'CNBC', 'channel_id': 'UCvJJ_dzjViJCoLf5uKUTwoA', 'view_count': 2800000, 'category': 'Haberler', 'duration': '12:33'},
    {'id': 'NG4Ws74RV04', 'title': 'Economy Update: Market Analysis', 'channel_title': 'Bloomberg', 'channel_id': 'UCIALMKvObZNtJ6AmdCLP7Lg', 'view_count': 1500000, 'category': 'Haberler', 'duration': '15:20'},
    {'id': 'V75dMMIW2B4', 'title': 'Climate Change: What You Need to Know', 'channel_title': 'Vox', 'channel_id': 'UCLXo7UDZvByw2ixzpQCufnA', 'view_count': 8900000, 'category': 'Haberler', 'duration': '11:15'},
    {'id': 'w8HdOHrc3OQ', 'title': 'Space Exploration: New Discoveries', 'channel_title': 'Veritasium', 'channel_id': 'UCHnyfMqiRRG1u-2MsSQLbXA', 'view_count': 12000000, 'category': 'Haberler', 'duration': '18:42'},
    
    # Sports
    {'id': 'NmGXhEJcVeo', 'title': 'Top 50 Goals of the Season 2024', 'channel_title': 'UEFA Champions League', 'channel_id': 'UCZ7E6MWMW1A8PxQTJV3Sdw', 'view_count': 45000000, 'category': 'Spor', 'duration': '22:15'},
    {'id': 'RYpBQNyPfJc', 'title': 'LeBron James - Career Highlights', 'channel_title': 'NBA', 'channel_id': 'UCWOF2KK9eE5V3ZQ4NYJP5KQ', 'view_count': 68000000, 'category': 'Spor', 'duration': '15:30'},
    {'id': 'KbN-TE2qpJc', 'title': 'Cristiano Ronaldo - Best Skills & Goals', 'channel_title': 'Football Daily', 'channel_id': 'UCQvdU45wisLu7RqfO3S3Dgw', 'view_count': 125000000, 'category': 'Spor', 'duration': '18:45'},
    {'id': 'HxXCgDhOaV4', 'title': 'Messi Magic - World Cup 2022', 'channel_title': 'FIFA', 'channel_id': 'UCWOA1ZGywLbqmigxE4Qlvuw', 'view_count': 180000000, 'category': 'Spor', 'duration': '12:20'},
    {'id': 'L7_jYl5vbWs', 'title': 'UFC Best Knockouts Compilation', 'channel_title': 'UFC', 'channel_id': 'UCvgfXK4nTYKudb0rFR6noLA', 'view_count': 32000000, 'category': 'Spor', 'duration': '25:10'},
    
    # Education
    {'id': 'fKopy74weus', 'title': 'How The Universe Works - Full Documentary', 'channel_title': 'Kurzgesagt', 'channel_id': 'UCsXVk37bltHxD1rDPwtNM8Q', 'view_count': 42000000, 'category': 'Eğitim', 'duration': '35:22'},
    {'id': 'aircAruvnKk', 'title': 'Learn Python in 1 Hour - Full Course', 'channel_title': 'Programming with Mosh', 'channel_id': 'UCWv7vMbMWH4-V0ZXdmDpPBA', 'view_count': 28000000, 'category': 'Eğitim', 'duration': '1:02:15'},
    {'id': 'rfscVS0vtbw', 'title': 'JavaScript Tutorial for Beginners', 'channel_title': 'freeCodeCamp', 'channel_id': 'UC8butISFwT-Wl7EV0hUK0BQ', 'view_count': 15000000, 'category': 'Eğitim', 'duration': '48:30'},
    {'id': 'dNLP3ofyc6s', 'title': 'History of Ancient Rome', 'channel_title': 'History Channel', 'channel_id': 'UC9MAhZQQd9egwWCxrwSIsJQ', 'view_count': 22000000, 'category': 'Eğitim', 'duration': '42:18'},
    {'id': 'ua8sSLvA8Mc', 'title': 'Understanding Quantum Physics', 'channel_title': 'PBS Space Time', 'channel_id': 'UC7_gcs09iThXybpVgjHZ_7g', 'view_count': 8500000, 'category': 'Eğitim', 'duration': '22:45'},
    {'id': 'WM1FFhaWq9Y', 'title': 'How to Start a Business in 2024', 'channel_title': 'Graham Stephan', 'channel_id': 'UCV6KDgJskWaEckne5aPA0aQ', 'view_count': 5200000, 'category': 'Eğitim', 'duration': '28:15'},
    
    # Comedy
    {'id': 'iik25wqIuFo', 'title': 'Try Not To Laugh Challenge - Impossible', 'channel_title': 'MrBeast', 'channel_id': 'UCX6OQ3DkcsbYNE6H8uQQuVA', 'view_count': 150000000, 'category': 'Komedi', 'duration': '16:42'},
    {'id': 'GP_0BhCw2rg', 'title': 'Stand Up Comedy Special', 'channel_title': 'Netflix Is A Joke', 'channel_id': 'UCRFo8wZvXPOHOfZ3tNQH9Sg', 'view_count': 42000000, 'category': 'Komedi', 'duration': '55:30'},
    {'id': '5Eqb_-j3FDA', 'title': 'Funny Fails Compilation 2024', 'channel_title': 'FailArmy', 'channel_id': 'UCPDis9pjXuqyI7RYLJ-TTSA', 'view_count': 85000000, 'category': 'Komedi', 'duration': '12:18'},
    {'id': 'At8v_Yc044Y', 'title': 'Prank Wars - Best Edition', 'channel_title': 'Dude Perfect', 'channel_id': 'UCRijo3ddMTht_IHyNSNXpNQ', 'view_count': 62000000, 'category': 'Komedi', 'duration': '18:25'},
    {'id': 'BQSsrvsszcs', 'title': 'Roast Me - Savage Comebacks', 'channel_title': 'All Def', 'channel_id': 'UCPDXXXJj9nax0fr0Wfc048g', 'view_count': 28000000, 'category': 'Komedi', 'duration': '22:10'},
    
    # Movies/Film
    {'id': 'JfVOs4VSpmA', 'title': 'Avatar 3 - Official Trailer', 'channel_title': '20th Century Studios', 'channel_id': 'UCzBPDsgameNxZtgqN-XPMqA', 'view_count': 125000000, 'category': 'Filmler', 'duration': '3:15'},
    {'id': 'zSWdZVtXT7E', 'title': 'Spider-Man: Beyond the Spider-Verse - Trailer', 'channel_title': 'Sony Pictures', 'channel_id': 'UCz3eeVAzq38MvEO5b7K26Jw', 'view_count': 98000000, 'category': 'Filmler', 'duration': '2:48'},
    {'id': 'aMQoMwj3zHo', 'title': 'Top 10 Movies of 2024', 'channel_title': 'CinemaBlend', 'channel_id': 'UC_RYn4n-Lzj3-0AtW8o_N_Q', 'view_count': 8500000, 'category': 'Filmler', 'duration': '18:30'},
    {'id': 'qEVUtrk8_B4', 'title': 'Behind The Scenes: Making of Avengers', 'channel_title': 'Marvel Entertainment', 'channel_id': 'UCvC4D8onUfXzvjTOM-dBfEA', 'view_count': 45000000, 'category': 'Filmler', 'duration': '25:15'},
    {'id': 'giXco2jaZ_4', 'title': 'The Batman - Complete Breakdown', 'channel_title': 'ScreenRant', 'channel_id': 'UCBq-pksCkq2N1PgWRG-AFLQ', 'view_count': 18000000, 'category': 'Filmler', 'duration': '32:45'},
    
    # Mix/Popular
    {'id': '9bZkp7q19f0', 'title': 'PSY - Gangnam Style', 'channel_title': 'officialpsy', 'channel_id': 'UCrDkAvwZum-UTjHmzDI2iIw', 'view_count': 5000000000, 'category': 'Mixler', 'duration': '4:13'},
    {'id': 'kffacxfA7G4', 'title': 'Baby Shark Dance - Kids Songs', 'channel_title': 'Pinkfong', 'channel_id': 'UCcdwLMPsaU2ezNSJU1nFoBQ', 'view_count': 14000000000, 'category': 'Mixler', 'duration': '2:16'},
    {'id': '2ZIpFytCSVc', 'title': 'BLACKPINK - How You Like That', 'channel_title': 'BLACKPINK', 'channel_id': 'UCOmHUn--16B90oW2L6FRR3A', 'view_count': 1100000000, 'category': 'Mixler', 'duration': '3:02'},
    {'id': 'Lrj2Hq7xqQ8', 'title': 'BTS - Dynamite', 'channel_title': 'HYBE LABELS', 'channel_id': 'UC3IZKseVpdzPSBaWxBxundA', 'view_count': 1800000000, 'category': 'Mixler', 'duration': '3:43'},
]


def get_sample_videos(query='', category='', max_results=50):
    """
    Get sample videos, optionally filtered by query or category.
    """
    videos = SAMPLE_VIDEOS.copy()
    
    # Filter by category if provided
    if category and category != 'Tümü':
        videos = [v for v in videos if v.get('category') == category]
    
    # Filter by search query if provided
    if query:
        query_lower = query.lower()
        videos = [v for v in videos if 
                  query_lower in v['title'].lower() or 
                  query_lower in v['channel_title'].lower()]
    
    # Shuffle to mix up the order
    random.shuffle(videos)
    
    # Add required fields for display
    result = []
    for video in videos[:max_results]:
        result.append({
            'id': video['id'],
            'title': video['title'],
            'description': f"Watch {video['title']} on VideoTube",
            'thumbnail': f"https://img.youtube.com/vi/{video['id']}/maxresdefault.jpg",
            'channel_title': video['channel_title'],
            'channel_id': video['channel_id'],
            'published_at': '2024-01-15T12:00:00Z',
            'view_count': video['view_count'],
            'like_count': int(video['view_count'] * 0.04),
            'youtube_url': f"https://www.youtube.com/watch?v={video['id']}",
            'duration': video.get('duration', '0:00'),
            'category': video.get('category', 'Tümü'),
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
                'part': 'snippet,statistics',
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
                    'part': 'snippet,statistics',
                    'id': ','.join(video_ids),
                }
                details_response = requests.get(details_url, params=details_params, timeout=10)
                details_response.raise_for_status()
                items = details_response.json().get('items', [])
        
        for item in items:
            video_id = item['id'] if isinstance(item['id'], str) else item['id'].get('videoId', '')
            snippet = item.get('snippet', {})
            statistics = item.get('statistics', {})
            
            # Get thumbnail - prefer high quality
            thumbnails = snippet.get('thumbnails', {})
            thumbnail_url = (
                thumbnails.get('maxres', {}).get('url') or
                thumbnails.get('high', {}).get('url') or
                thumbnails.get('medium', {}).get('url') or
                thumbnails.get('default', {}).get('url', '')
            )
            
            videos.append({
                'id': video_id,
                'title': snippet.get('title', 'Untitled'),
                'description': snippet.get('description', ''),
                'thumbnail': thumbnail_url,
                'channel_title': snippet.get('channelTitle', 'Unknown'),
                'channel_id': snippet.get('channelId', ''),
                'published_at': snippet.get('publishedAt', ''),
                'view_count': int(statistics.get('viewCount', 0)),
                'like_count': int(statistics.get('likeCount', 0)),
                'youtube_url': f'https://www.youtube.com/watch?v={video_id}',
            })
        
        return videos
    
    except requests.RequestException as e:
        print(f"YouTube API error: {e}")
        return get_sample_videos(query=query, category=category, max_results=max_results)
    except (KeyError, ValueError) as e:
        print(f"Error parsing YouTube response: {e}")
        return get_sample_videos(query=query, category=category, max_results=max_results)


def get_video_details(video_id):
    """
    Get detailed information about a specific YouTube video.
    """
    if not YOUTUBE_API_KEY:
        # Return from sample videos if available
        for video in SAMPLE_VIDEOS:
            if video['id'] == video_id:
                return {
                    'id': video['id'],
                    'title': video['title'],
                    'description': f"Watch {video['title']} on VideoTube",
                    'thumbnail': f"https://img.youtube.com/vi/{video['id']}/maxresdefault.jpg",
                    'channel_title': video['channel_title'],
                    'channel_id': video['channel_id'],
                    'published_at': '2024-01-15T12:00:00Z',
                    'view_count': video['view_count'],
                    'like_count': int(video['view_count'] * 0.04),
                    'comment_count': int(video['view_count'] * 0.001),
                    'duration': video.get('duration', 'PT0M0S'),
                    'youtube_url': f"https://www.youtube.com/watch?v={video['id']}",
                }
        return None
    
    try:
        url = f'{YOUTUBE_API_BASE_URL}/videos'
        params = {
            'key': YOUTUBE_API_KEY,
            'part': 'snippet,statistics,contentDetails',
            'id': video_id,
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('items', [])
        if not items:
            return None
        
        item = items[0]
        snippet = item.get('snippet', {})
        statistics = item.get('statistics', {})
        content_details = item.get('contentDetails', {})
        
        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = (
            thumbnails.get('maxres', {}).get('url') or
            thumbnails.get('high', {}).get('url') or
            thumbnails.get('medium', {}).get('url', '')
        )
        
        return {
            'id': video_id,
            'title': snippet.get('title', 'Untitled'),
            'description': snippet.get('description', ''),
            'thumbnail': thumbnail_url,
            'channel_title': snippet.get('channelTitle', 'Unknown'),
            'channel_id': snippet.get('channelId', ''),
            'published_at': snippet.get('publishedAt', ''),
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'duration': content_details.get('duration', 'PT0M0S'),
            'youtube_url': f'https://www.youtube.com/watch?v={video_id}',
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
