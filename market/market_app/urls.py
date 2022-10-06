from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('compare/', views.CompareView.as_view(), name='compare'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('history_order/', views.HistoryOrderView.as_view(), name='historyorder'),
    path('history_view/', views.HistoryViewView.as_view(), name='historyview'),
    path('oneorder/', views.OneOrderView.as_view(), name='oneorder'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('payment_someone/', views.PaymentSomeOneView.as_view(), name='payment_someone'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile_avatar/', views.ProfileAvatarView.as_view(), name='profile_avatar'),
    path('progress_payment/', views.ProgressPaymentView.as_view(), name='progress_payment'),
    path('sale/', views.SaleView.as_view(), name='sale'),
    path('shop/', views.ShopView.as_view(), name='shop'),
]
