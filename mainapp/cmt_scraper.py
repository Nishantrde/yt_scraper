# Required libraries
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
import emoji


def get_data(vid):
    vid_id = vid
    yt_client = build(
        "youtube", "v3", developerKey="AIzaSyBStzjdyRbMp68HN9Td2SQTXmI25kKxQoU"
    )

    def get_comment(client, video_id, token=None):
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

    def clean_text(text):
        text = re.sub(r'["]', '', text)  # Remove inverted commas
        text = emoji.replace_emoji(text, replace="")  # Remove emojis
        return text

    comments = []
    next = None

    while True:
        resp = get_comment(yt_client, vid_id, next)
        if not resp:
            break
        comments += resp["items"]
        next = resp.get("nextPageToken")
        if not next:
            break

    print(f"Total cmts fetched: {len(comments)}")

    notes = ""
    for comment in comments:
        comment_text = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        single_line_comment = comment_text.replace("\n", ".")
        cleaned_comment = clean_text(single_line_comment)
        notes += f"{cleaned_comment}. "

    data = {
        "texts": [notes]
    }
    
    # Return the LDA HTML content generated by the analysis function
    return analysis(data)


