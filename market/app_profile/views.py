from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from app_login.models import Profile, ProfileAvatar
from app_profile.forms import ProfileForm
from market_app.product_history import HistoryViewOperations


class AccountView(TemplateView):

    """Личный кабинет"""

    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with HistoryViewOperations(self.request.user) as history:
            history_view_list = history.products()[:3]
        context['middle_title_left'] = 'Личный кабинет'
        context['middle_title_right'] = 'Личный кабинет'
        context['active_menu'] = 'account'
        context['history_view_list'] = history_view_list
        context['profile'] = Profile.objects.get(user_id=self.request.user.id)

        return context


class ProfileView(View):

    """Профиль пользователя"""

    def get(self, request):

        profile_form = ProfileForm()

        return render(request, 'profile.html', context={'profile_form': profile_form,
                                                        'middle_title_left': 'Профиль',
                                                        'middle_title_right': 'Профиль',
                                                        'active_menu': 'profile'})

    def post(self, request):

        profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():

            avatar = profile_form.cleaned_data.pop('avatar')
            new_password1 = profile_form.cleaned_data.pop('new_password1')
            new_password2 = profile_form.cleaned_data.pop('new_password2')

            if avatar:
                ProfileAvatar.objects.create(avatar=avatar, img_name=f'{avatar}')
                profile_avatar = ProfileAvatar.objects.get(img_name=f'{avatar}')
                Profile.objects.filter(user_id=request.user.id).update(
                    avatar=profile_avatar
                )
            elif new_password1:
                if new_password1 == new_password2:
                    # user = User.objects.get(id=request.user.id)
                    # user.set_password(new_password1)
                    print('Password change')
                else:
                    raise Exception('Password not correct')

            for key in profile_form.cleaned_data.keys():

                if key == 'full_name' and profile_form.cleaned_data.get(key):
                    Profile.objects.filter(id=request.user.id).update(full_name=profile_form.cleaned_data[key])

                elif key == 'email' and profile_form.cleaned_data.get(key):
                    User.objects.filter(id=request.user.id).update(email=profile_form.cleaned_data[key])

                elif key == 'phone' and profile_form.cleaned_data.get(key):
                    Profile.objects.filter(id=request.user.id).update(phone=profile_form.cleaned_data[key])

            return HttpResponseRedirect('/account/')

        return render(request, 'profile.html', context={'profile_form': profile_form,
                                                        'middle_title_left': 'Профиль',
                                                        'middle_title_right': 'Профиль',
                                                        'active_menu': 'profile'})
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['middle_title_left'] = 'Профиль'
    #     context['middle_title_right'] = 'Профиль'
    #     context['active_menu'] = 'profile'


class HistoryOrderView(TemplateView):

    """История заказов пользователя"""

    template_name = 'historyorder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['middle_title_left'] = 'История заказов'
        context['middle_title_right'] = 'История заказов'
        context['active_menu'] = 'historyorder'
        return context


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
