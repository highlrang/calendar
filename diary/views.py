from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic import *
from schedule.models import Diary, Category
from mysite.views import OwnerOnlyMixin, OwnerCategoryCheck
from .forms import DiaryForm

# Create your views here.

# 일기

#DayArchiveView
def Diary_date(request, cate, date):
    day_list = Diary.objects.filter(d_cate=cate, d_date = date)
    return render(request, 'diary/diary_day_list.html', {'day_list':day_list, 'date':date, 'category': cate})


class DiaryDV(DetailView):
    model = Diary
    template_name = 'diary/diary_detail.html'



class DiaryCV(OwnerCategoryCheck, CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['cate']
        context['date'] = self.kwargs['date']
        return context

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.d_user = self.request.user
        form.save()

        object_list = Category.objects.filter(c_user = self.request.user)
        return render(self.request, 'home.html', {'object_list': object_list, 'passCateId': self.kwargs['cate']})


class DiaryUV(OwnerOnlyMixin, UpdateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_update.html'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.d_user = self.request.user
        form.save()

        object_list = Category.objects.filter(c_user=self.request.user)
        return render(self.request, 'home.html', {'object_list': object_list, 'passCateId': self.kwargs['cate']})


def DiaryDel(request, pk, cate, date):
    object = Diary.objects.get(d_id=pk)
    if object.d_user == request.user:
        object.delete()
        msg = '삭제되었습니다.'
    else:
        msg = '소유자만 접근 가능합니다.'
    return HttpResponseRedirect(reverse('diary:diaryDate', kwargs={'cate':cate, 'date':date, 'msg': msg}))


