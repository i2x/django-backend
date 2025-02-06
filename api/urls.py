from django.urls import path
from .views import (
    GoogleLoginView,
    CurriculumCoursesView,
    CourseListView,
    NoteListCreateView,
    NoteDetailView,
    NoteSearchView
)




urlpatterns = [
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('curriculum/', CurriculumCoursesView.as_view(), name='curriculum-latest'),  # Get latest curriculum courses


    # 🎯 Course API
    path("courses/", CourseListView.as_view(), name="course-list"),

    # 🎯 Note APIs
    path("notes/", NoteListCreateView.as_view(), name="note-list-create"),  # List & Create
    path("notes/<int:pk>/", NoteDetailView.as_view(), name="note-detail"),  # Retrieve, Update, Delete
    path("notes/search/", NoteSearchView.as_view(), name="note-search"),  # Search Notes


]





