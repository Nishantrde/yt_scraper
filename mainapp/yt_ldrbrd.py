# Required libraries
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re


def get_data_lk(vid):
    vid_id = vid
    yt_client = build(
        "youtube", "v3", developerKey="AIzaSyBStzjdyRbMp68HN9Td2SQTXmI25kKxQoU",
    )
    def gen_data(client, video_id, token = None):
        try:
            response = (
                client.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    textFormat="plainText",
                    maxResults=3000,
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
    comments = []
    next = None

    while True:
        resp = gen_data(yt_client, vid_id, next)
        if not resp:
            break
        comments += resp["items"]
        next = resp.get("nextPageToken")
        if not next:
            break

    print(f"Total cmts_info fetched: {len(comments)}")

    base = {}
    

    for comment in comments:
        user_id = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        like_count = comment["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        reply_count = comment["snippet"]["totalReplyCount"]
        snippet = comment["snippet"]["topLevelComment"]["snippet"]

        user_info = {"likes": like_count, "ReplyCount": reply_count, "snippet": snippet}
        base[user_id] = user_info
    
    base = sorted(base.items(), key=lambda x: x[1]['likes'], reverse=True)
    
    return base

def get_data_rpc(vid):
    vid_id = vid
    yt_client = build(
        "youtube", "v3", developerKey="AIzaSyBStzjdyRbMp68HN9Td2SQTXmI25kKxQoU",
    )
    def gen_data(client, video_id, token = None):
        try:
            response = (
                client.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    textFormat="plainText",
                    maxResults=3000,
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
    comments = []
    next = None

    while True:
        resp = gen_data(yt_client, vid_id, next)
        if not resp:
            break
        comments += resp["items"]
        next = resp.get("nextPageToken")
        if not next:
            break

    print(f"Total cmts_info fetched: {len(comments)}")

    base = {}
    

    for comment in comments:
        user_id = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        like_count = comment["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        reply_count = comment["snippet"]["totalReplyCount"]
        snippet = comment["snippet"]["topLevelComment"]["snippet"]

        user_info = {"likes": like_count, "ReplyCount": reply_count, "snippet": snippet}
        base[user_id] = user_info
    
    base = sorted(base.items(), key=lambda x: x[1]['ReplyCount'], reverse=True)
    
    return base


# get_data_id("RBhCq3jF-Xs")





        