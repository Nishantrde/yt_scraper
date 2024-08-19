from django.shortcuts import render
from .cmt_scraper import *
from .yt_ldrbrd import *

def index(request):
    lda_html_content = None
    lrbd = None
    rep_cnt = None
    
    if request.method == "POST":
        
        if request.POST.get('lb'):
            video_id = request.POST.get('video-id')
            lrbd = list(get_data_lk(video_id))[:10]
            rep_cnt = list(get_data_rpc(video_id))[:10]
            return render(request, 'yt_leader_brd.html' , {"lrbd": lrbd, "rep_cnt": rep_cnt})

    return render(request, "index.html")
            
         

    
