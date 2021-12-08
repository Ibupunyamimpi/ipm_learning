from django.urls import path
from .views import CourseListView, CourseDetailView, ContentDetailView, CourseLibraryView

app_name = "content"

urlpatterns = [
    path("explore/", CourseListView.as_view(), name="course-list"),
    path("library/", CourseLibraryView.as_view(), name="course-library"),
    path("<slug>/", CourseDetailView.as_view(), name="course-detail"),
    path("<slug>/<content_slug>/", ContentDetailView.as_view(), name="content-detail"),
]
