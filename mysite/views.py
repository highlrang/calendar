from django.views.generic import TemplateView, CreateView, ListView
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy, reverse
from schedule.models import Category


class HomeView(ListView):
    model = Category
    template_name = 'home.html'

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return
        else:
            return Category.objects.filter(c_user=self.request.user)

def Before_Home(request, cate):
    object_list = Category.objects.filter(c_user=request.user)
    return render(request, 'home.html', {'object_list': object_list, 'passCateId': cate})



class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'


class UserSignOut(TemplateView):
    template_name = 'registration/sign_out.html'

def UserSignOut_done(request):
    user = User.objects.get(request.user)
    user.delete()
    return HttpResponseRedirect(reverse('home'))


class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "소유자만 접근할 수 있습니다."

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        category = Category.objects.get(c_id=self.kwargs['cate'])
        if category.c_diary == True:
        # diary
            if request.user != obj.d_user:
                return self.handle_no_permission()
        # schedule
        else:
            if request.user != obj.s_user:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class OwnerCategoryCheck(AccessMixin):
    raise_exception = True
    permission_denied_message = "접근할 수 없습니다."

    def dispatch(self, request, *args, **kwargs):
        category = Category.objects.get(c_id=self.kwargs['cate'])
        if request.user != category.c_user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class user_settings(TemplateView):
    template_name = 'settings.html'

"""
def bad_request(request, exception):
    return render(request, "error.html", status=400)
def permission_denied(request, exception):
    return render(request, "error.html", status=403)
def page_not_found(request, exception):
    return render(request, "error.html", status=404)
def server_error(request):
    return render(request, "error.html", status=500)
"""