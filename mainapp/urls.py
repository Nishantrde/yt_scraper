from django.urls import path, include
from .views import *

urlpatterns = [
    path("", index),
    path("yt_top_CATEGORY", analy),
    path("yt_top_SALIENT", top_analy),
    path("yt_lda_model", lda_vis),
]

