from django.shortcuts import render
from django.views.generic import TemplateView
from app_login.models import Profile
from market_app.product_history import HistoryViewOperations


class AccountView(TemplateView):
    """Личный кабинет"""
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with HistoryViewOperations(self.request.user) as history:
            history_view_list = history.products()[:3]
        full_name = [name.full_name for name in Profile.objects.filter(user_id=self.request.user.id).only('full_name')]
        context['middle_title_left'] = 'Личный кабинет'
        context['middle_title_right'] = 'Личный кабинет'
        context['active_menu'] = 'account'
        context['history_view_list'] = history_view_list
        context['full_name'] = full_name[0]
        return context


class ProfileView(TemplateView):
    """Профиль пользователя"""
    template_name = 'profile.html'
    extra_context = {
        'middle_title_left': 'Профиль',
        'middle_title_right': 'Профиль',
        'active_menu': 'profile',
    }


class HistoryOrderView(TemplateView):
    """История заказов пользователя"""
    template_name = 'historyorder.html'
    extra_context = {
        'middle_title_left': 'История заказов',
        'middle_title_right': 'История заказов',
        'active_menu': 'historyorder',
    }


class HistoryViewView(TemplateView):
    """История просмотров пользователя"""
    template_name = 'historyview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with HistoryViewOperations(self.request.user) as history:
            history_view_list = history.products()
        context['middle_title_left'] = 'История просмотра'
        context['middle_title_right'] = 'История просмотра'
        context['active_menu'] = 'historyview'
        context['history_view_list'] = history_view_list
        return context