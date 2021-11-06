from django.urls import path
from . import views 

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('cards/', views.CardDetailView.as_view(), name='card_details'),
    path('cards/<int:pk>/', views.CardDetailRetrieveUpdateView.as_view(), name='card_update_retrieve'),
    path('config/', views.StripeConfig.as_view()),
    path('create-checkout-session/', views.CreateCheckoutSession.as_view()),
    path('success/', views.PaymentSuccess.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
    # path('webhook/', views.stripe_webhook),#
]   