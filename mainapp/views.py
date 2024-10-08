from django.shortcuts import render
from .cmt_scraper import *
from .yt_ldrbrd import *
from .multi_vid_cmt_scpr import *
from .tester import scraper
from collections import Counter
import json
from .json_fl import *

def calculate_user_frequencies(lrbd, rep_cnt):
    users = []

    for item in lrbd:
        users.append(item.get('user'))

    for item in rep_cnt:
        users.append(item.get('user'))

    user_frequencies = Counter(users)
    
    filtered_user_frequencies = {user: freq for user, freq in user_frequencies.items() if freq > 1}
    
    return filtered_user_frequencies

def index(request):
    lrbd = None
    rep_cnt = None
    graph_data = None  # Variable to hold graph data
    
    if request.method == "POST":
        if request.POST.get('lb'):
            video_id = request.POST.get('video-id')
            lrbd = list(get_data_lk(video_id))[:10]
            
            rep_cnt = list(get_data_rpc(video_id))[:10]
            
            return render(request, 'yt_leader_brd.html', {"lrbd": lrbd, "rep_cnt": rep_cnt})

    if request.GET.get('mltv'):
            return render(request, "multi_scraper.html")
    if request.POST.get('mltv'):
            video_ids = str(request.POST.get('video-ids'))
            video_ids = video_ids.split(",")
            u_info = scraper(video_ids)

            total_cmts = u_info[1]
            videos = u_info[2]

            print(u_info[1:])
            u_info = u_info[0]

            # Prepare data for the graph
            user_names = list(u_info.keys())
            comment_counts = [info['no_comments'] for info in u_info.values()]

            graph_data = {
                'labels': user_names,
                'data': comment_counts,
            }

            # Prepare video data for template
            video_data = [
                {
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail_url': f"https://img.youtube.com/vi/{video_id}/0.jpg",
                    'comment_count': comment_count
                }
                for video_id, comment_count in videos.items()
            ]

            return render(request, "multi_scraper_view.html", {
                "u_info": u_info,
                "graph_data": json.dumps(graph_data),
                "video_data": video_data,  # Pass the video data to the template
                "total_cmts": total_cmts
            })

    return render(request, "index.html")

def analy(request):
    # print(json_f)
    return render(request, "anayl.html", {"json_data" : json_f})

def top_analy(request):
    categories = list(json_f_top_30.keys())
    frequencies = [json_f_top_30[category]['frequency'] for category in categories]
    comments = {category: json_f_top_30[category]['comments'][:int(len(json_f_top_30[category]['comments'])*(50/100))] for category in categories}
    print(comments)
    context = {
        'categories': categories,
        'frequencies': frequencies,
        'comments': comments,
    }

    
    return render(request, "top_analy.html", context)


def lda_vis(request):
    return render(request, "lda_vis.html")


