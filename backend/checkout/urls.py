from django.urls import path, include
from .views import LinkAPIView, OrderAPIView, test_payment

urlpatterns = [
    path('links/<str:code>', LinkAPIView.as_view()), 
    path('orders', OrderAPIView.as_view()),
    path('test/payments', test_payment)
]