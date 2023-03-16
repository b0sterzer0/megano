from django.urls import path
from .views import AccountView, ProfileView, HistoryOrderView, HistoryViewView

urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('edit/', ProfileView.as_view(), name='profile'),
    path('history_order/', HistoryOrderView.as_view(), name='historyorder'),
    path('history_view/', HistoryViewView.as_view(), name='historyview'),
]
