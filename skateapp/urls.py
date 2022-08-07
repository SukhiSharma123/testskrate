from django.urls import include, path
from .views import *

urlpatterns = [
    path('new', TicketAPIView.as_view(), name='tickets'),
    path('all', TicketAPILISTView.as_view(), name='tickets'),
    path('markAsClosed', markAsClosedView.as_view(), name='close'),
    path('delete', markAsClosedView.as_view(), name='delete'),
]