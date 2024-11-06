from django.urls import path

from .views import UserStatisticsView


app_name = "stats"

urlpatterns = [
    path(
        "user-statistics/", UserStatisticsView.as_view(), name="user-statistics"
    ),
]
