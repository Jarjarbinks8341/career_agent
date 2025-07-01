from django.urls import path
from .views import CVSuggestionView

urlpatterns = [
    path('suggest/', CVSuggestionView.as_view(), name='cv-suggest'),
] 