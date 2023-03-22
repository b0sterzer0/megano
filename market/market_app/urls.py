from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('account/', views.AccountView.as_view(), name='account'),
    # path('carts/', views.CartView.as_view(), name='cart'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('comparison/', include('compare_app.urls')),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('history_order/', views.HistoryOrderView.as_view(), name='historyorder'),
    path('history_view/', views.HistoryViewView.as_view(), name='historyview'),
    path('order/', include('order_app.urls')),
    path('product/<int:pk>/', views.ProductView.as_view(), name='product'),
    path('payment/', include('payment_app.urls')),
    path('APIPayment/', include('api_for_payment_app.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile_avatar/', views.ProfileAvatarView.as_view(), name='profile_avatar'),
    path('sale/', views.SaleView.as_view(), name='sale'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('seller/<int:pk>/', views.SellerDetailView.as_view(), name='seller'),
]
