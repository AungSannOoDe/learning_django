from django.urls import path,include
from to_do_app.api.views import MovieView, MovieViewDetail,WatchViewList,WatchDetailView,StreamViewList,StreamDetailView,ReviewList,ReviewDetail,ReviewCreate,StreamPlatformVS
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("stream",StreamPlatformVS,basename="streamplatform")

urlpatterns = [
    # Movies endpoints
    path("movies/", MovieView.as_view(), name="movie_list"),
    path("movies/<int:pk>/", MovieViewDetail.as_view(), name="movie_detail"),
    path("",include(router.urls)),
    # # Streaming Platforms endpoints
    # path("stream/", StreamViewList.as_view(), name="platform_list"),
    # path("stream/<int:pk>/", StreamDetailView.as_view(), name="platform_detail"),
    # WatchList endpoints
    path("watchlist/", WatchViewList.as_view(), name="watch_list"),
    path("watchlist/<int:pk>/", WatchDetailView.as_view(), name="watch_detail"),
    # path("review/",ReviewList.as_view(),name="review-list"),
    # path("review/<int:pk>",ReviewDetail.as_view(),name="review-detail"),
    path("stream/review/<int:pk>", ReviewDetail.as_view(), name="platform_list"),
    path("stream/<int:pk>/review", ReviewList.as_view(), name="platform_detail"),
    path("stream/<int:pk>/review-create",ReviewCreate.as_view() , name="review_create"),

]