from django.urls import path
from .views import CardDetailRetrieveUpdateView, CardDetailView

urlpatterns = [
    path('cards/', CardDetailView.as_view(), name='card_details'),
    path('cards/<int:pk>/', CardDetailRetrieveUpdateView.as_view(), name='card_update_retrieve')
]