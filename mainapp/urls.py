from django.urls import path, include
from .views import *

urlpatterns = [
    path("", index),
    path("yt_analyser", analy),
    path("yt_top_analyser", top_analy),
    path("yt_lda_model", lda_vis),
]

