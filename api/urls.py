from django.urls import path
from .views import GoogleLoginView,SearchFilesView

urlpatterns = [
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('search/', SearchFilesView.as_view(), name='search-files'),

]


