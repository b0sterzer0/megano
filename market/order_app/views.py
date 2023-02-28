from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User

from app_login.models import Profile


class OrderView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            context = {}
        else:
            try:
                profile = Profile.objects.get(user=request.user)
                user_email = User.objects.get(id=request.user.id).email
                context = {'full_name': profile.full_name,
                           'phone': profile.phone,
                           'email': user_email}
            except ObjectDoesNotExist:
                return HttpResponse('Не удалось получить данные пользователя')

        return render(request, 'order.html', context=context)

    def post(self, request):
        pass
