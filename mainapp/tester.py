from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .yt_api import api_key
import re

def scraper(vid):
    video_id = vid
    yt_scraper = build(
        "youtube", "v3", developerKey=api_key
    )

    def get_comment(client, video_id, token=None):
        try:
            response = (
                client.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    textFormat="plainText",
                    maxResults=100,
                    pageToken=token,
                ).execute()
            )
            return response
        except HttpError as e:
            print(e.resp.status)
            return None
        except Exception as e:
            print(e)
            return None

    def clean_text(text):
        text = re.sub(r'["]', '', text)
        return text

    user_info = {}
    comments = []
    next = None

    for id in video_id:
        while True:
            resp = get_comment(yt_scraper, id, next)
            if not resp:
                break
            comments += resp["items"]
            next = resp.get("nextPageToken")
            if not next:
                break
        print(f"Cmts fetched: {len(comments)}")

    for comment in comments:
        user_id = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        comment_text = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        likes = comment["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        single_line_comment = comment_text.replace("\n", ".")
        cleaned_comment = clean_text(single_line_comment)
        
        if user_id not in user_info:
            user_info[user_id] = {
                "no_comments": 1,
                "comment": [cleaned_comment],
                "likes": [likes],
                "snippet": [comment["snippet"]["topLevelComment"]["snippet"]],
                "image_url": comment["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"],
            }
        else:
            user_info[user_id]["no_comments"] += 1
            user_info[user_id]["comment"].append(cleaned_comment)
            user_info[user_id]["likes"].append(likes)
            user_info[user_id]["snippet"].append(comment["snippet"]["topLevelComment"]["snippet"])

    # Remove users with only one comment
    user_info = {user: info for user, info in user_info.items() if info["no_comments"] > 1}

    # Sort the user_info dictionary by the number of comments
    user_info = dict(sorted(user_info.items(), key=lambda item: item[1]["no_comments"], reverse=True))

    print(f"Total cmts fetched: {len(comments)}")

    return [user_info]
