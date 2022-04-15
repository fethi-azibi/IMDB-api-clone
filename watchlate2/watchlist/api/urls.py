from django.urls import path
from . import views

'''urlpatterns = [
    path("list/", views.movie_list, name="movie_list"),
    path("<int:pk>/", views.single_movie, name="single_movie"),
]'''

urlpatterns = [
    path("list/", views.WatchListAV.as_view(), name="movie_list"),
    path("<int:pk>/", views.WatchListDetailAV.as_view(), name="single_movie"),
    path("stream/", views.PlatformStreamAV.as_view(), name="stream"),
    path("stream/<int:pk>", views.PlatformStreamDetail.as_view(), name="stream_detail"),
    # path("review/", views.ReviewList.as_view(), name="review-list"),
    # path("review/<int:pk>", views.ReviewDetail.as_view(), name="review-detail"),
    path("<int:pk>/reviews", views.ReviewList.as_view(), name="review-list"),
    path("review/<int:pk>", views.ReviewDetail.as_view(), name="review-detail"),
    path("<int:pk>/review-create", views.ReviewCreate.as_view(), name="review-create"),
    path("lists/", views.WatchListGV.as_view(), name="lists"),


]
