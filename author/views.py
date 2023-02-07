from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileUpdate
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from services import queryset
import json
# Create your views here.


@method_decorator(login_required, name='dispatch')
class UpProf(generic.UpdateView):
    template_name = 'upprof.html'
    form_class = ProfileUpdate

    def get(self, request, *args: str, **kwargs):
        user = Profile.objects.get(user=request.user)
        user_now = Profile.objects.get(slug=self.kwargs.get('slug'))
        if user != user_now:
            return render(request, 'exception_upprof.html')
        return super().get(request, *args, **kwargs)

    def get_object(self):
        kp = self.kwargs.get('slug')
        return get_object_or_404(Profile, slug=kp)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('love:home_urls')


class UsersClass(DetailView):
    template_name = 'users_detail.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        kp = self.kwargs.get('slug')
        user = Profile.objects.get(slug=kp)
        percent_cat = user.get_sum_category().items()

        context = {
            'user': user,

        }
        for cat, total in percent_cat:
            context[cat] = total

        data = get_series(context)
        data_ser = data[0]
        if data_ser == '[]':
            data_ser = False
        data_clear = data[1]

        context['data_ser'] = data_ser
        context['data_clear'] = data_clear
        context['user_now'] = request.user
        return render(request, self.template_name, context)


def users_view(request):
    users = queryset.all_profile()
    user = queryset.get_profile(request.user)

    context = {
        'users': users,
        'user': user,
    }

    return render(request, 'users.html', context)


def get_series(context):
    data_ser = []

    for i in context:
        if i in ['Грусть', "Пошлость", "Смех", "Любовь", "Сарказм"]:
            data_ser.append({
                'value': context[i][1],
                'category': i,
            })

    data_clear = sorted(data_ser, key=lambda d: d['value'], reverse=True)
    data_ser = json.dumps(data_ser)

    return (data_ser, data_clear)
