from googleapiclient.discovery import build
from collections import defaultdict

# Initialize the YouTube API client
def get_youtube_client(api_key):
    return build('youtube', 'v3', developerKey=api_key)

# Function to fetch comments for a given video ID
def fetch_comments(youtube, video_id):
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100
    )
    
    while request:
        response = request.execute()
        for item in response.get('items', []):
            comment_snippet = item['snippet']['topLevelComment']['snippet']
            comment = {
                'author': comment_snippet['authorDisplayName'],
                'like_count': comment_snippet['likeCount'],
                'text': comment_snippet['textDisplay']
            }
            comments.append(comment)
        
        request = youtube.commentThreads().list_next(request, response)
    
    return comments

# Function to aggregate comments and likes
def aggregate_comments(youtube, video_ids):
    user_stats = defaultdict(lambda: {'total_comments': 0, 'total_likes': 0, 'video_count': 0})

    for video_id in video_ids:
        comments = fetch_comments(youtube, video_id)
        users_commented = set()

        for comment in comments:
            author = comment['author']
            user_stats[author]['total_comments'] += 1
            user_stats[author]['total_likes'] += comment['like_count']
            users_commented.add(author)
        
        for user in users_commented:
            user_stats[user]['video_count'] += 1
    
    # Sort users by the number of videos commented on (descending)
    sorted_users = sorted(user_stats.items(), key=lambda x: x[1]['video_count'], reverse=True)
    
    return sorted_users

def main(api_key, video_ids):
    youtube = get_youtube_client(api_key)
    sorted_users = aggregate_comments(youtube, video_ids)

    # Display the results
    for user, stats in sorted_users:
        print(f"User: {user}")
        print(f"  Total Comments: {stats['total_comments']}")
        print(f"  Total Likes: {stats['total_likes']}")
        print(f"  Videos Commented On: {stats['video_count']}")
        print()

if __name__ == "__main__":
    API_KEY = 'YOUR_YOUTUBE_API_KEY'
    VIDEO_IDS = ['VIDEO_ID_1', 'VIDEO_ID_2', 'VIDEO_ID_3']  # Replace with your list of video IDs

    main(API_KEY, VIDEO_IDS)
