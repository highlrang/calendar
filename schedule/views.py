from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.db.models import Q
from mysite.views import OwnerOnlyMixin, OwnerCategoryCheck
from .models import *
from .forms import *
import datetime
import calendar
from calendar import HTMLCalendar


# Create your views here.
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, category=None):
        self.year = year
        self.month = month
        self.category = category
        super(Calendar, self).__init__()

    def formatday(self, day):
        todo_list = ''

        if day != 0:
            #print(self.year, self.month, day)
            date = datetime.date(self.year, self.month, day)
            todo_list = Schedule.objects.filter(Q(s_cate=self.category), Q(s_startDate=date) | Q(s_endDate=date) | Q(s_startDate__lt=date) & Q(s_endDate__gt=date)).order_by('-s_busy')

        d = ''
        if todo_list:
            # 일정 개수 자르기
            if len(todo_list) > 3:
                for i in range(0, 3):
                    # 기념일 확인
                    if todo_list[i].s_red == True:
                        # 완료여부 확인
                        if todo_list[i].s_complete == True:
                            d += f"<li class='scheRed scheComplete'>"
                        else:
                            d += f"<li class='scheRed'>"
                    else:
                        if todo_list[i].s_complete == True:
                            d += f"<li class='sche scheComplete'>"
                        else:
                            d += f"<li class='sche'>"

                    # 일정 글자수 자르기
                    if len(todo_list[i].s_content) > 4:
                        d += f"{todo_list[i].s_content[:4]}</li><br>"
                    else:
                        d += f"{todo_list[i].s_content}</li><br>"

            else:
                for todo in todo_list:
                    # 기념일 확인
                    if todo.s_red == True:
                        if todo.s_complete == True:
                            d += f"<li class='scheRed scheComplete'>"
                        else:
                            d += f"<li class='scheRed'>"
                    else:
                        if todo.s_complete == True:
                            d += f"<li class='sche scheComplete'>"
                        else:
                            d += f"<li class='sche'>"

                    # 일정 글자수 자르기
                    if len(todo.s_content) > 4:
                        d += f"{todo.s_content[:4]}</li><br>"
                    else:
                        d += f"{todo.s_content}</li><br>"

        if day != 0:
            return f"<td style='text-align: center; vertical-align: top;' ondblclick='location.href=\"/schedule/{self.category}/{date}/\"'><span class='date'>{day}</span><br><ul>{d}</ul></td>"
        return "<td></td>"

    def formatweek(self, theweek):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d)
        return f'<tr height=100px> {week} </tr>'

    def formatweekday(self, day):
        return '<th class="%s">%s</th>' % (day, day)

    def formatweekheader(self):
        s = ''.join(self.formatweekday(i) for i in ["일", "월", "화", "수", "목", "금", "토"])
        return '<tr>%s</tr>' % s

    def formatmonth(self, withyear=True):
        cal = f'<table class="calendar" width="100%" style="table-layout: fixed">\n'
        cal += f'<tr><th colspan="7" class="month">{str(self.year) + "년 " + str(self.month) + "월"}</th></tr>\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week)}\n'
        return cal




class Dalendar(HTMLCalendar):
    def __init__(self, year=None, month=None, category=None):
        self.year = year
        self.month = month
        self.category = category
        super(Dalendar, self).__init__()

    def formatday(self, day):
        diary_list = ''

        if day != 0:
            #print(self.year, self.month, day)
            date = datetime.date(self.year, self.month, day)
            diary_list = Diary.objects.filter(d_cate=self.category, d_date=date)

        d = ''
        if diary_list:
            if len(diary_list) > 3:
                for i in range(0, 3):
                    # 일정 글자수 자르기
                    if len(diary_list[i].d_title) > 4:
                        d += f"{diary_list[i].d_title[:4]}</li><br>"
                    else:
                        d += f"{diary_list[i].d_title}</li><br>"

            else:
                for diary in diary_list:
                    # 제목 글자수 자르기
                    if len(diary.d_title) > 4:
                        d += f"{diary.d_title[:4]}</li><br>"
                    else:
                        d += f"{diary.d_title}</li><br>"

        if day != 0:
            return f"<td style='text-align: center; vertical-align: top;' ondblclick='location.href=\"/diary/{self.category}/{date}/\"'><span class='date'>{day}</span><br><ul>{d}</ul></td>"
        return "<td></td>"

    def formatweek(self, theweek):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d)
        return f'<tr height=100px> {week} </tr>'

    def formatweekday(self, day):
        return '<th class="%s">%s</th>' % (day, day)

    def formatweekheader(self):
        s = ''.join(self.formatweekday(i) for i in ["일", "월", "화", "수", "목", "금", "토"])
        return '<tr>%s</tr>' % s

    def formatmonth(self, withyear=True):
        cal = f'<table class="calendar" width="100%" style="table-layout: fixed">\n'
        cal += f'<tr><th colspan="7" class="month">{str(self.year) + "년 " + str(self.month) + "월"}</th></tr>\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week)}\n'
        return cal










def get_date(date):
    if date:
        year, month = (int(i) for i in date.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(date):
    first = date.replace(day=1)
    prev = first - datetime.timedelta(days=1)
    month = str(prev.year) + '-' + str(prev.month)
    return month

def next_month(date):
    days = calendar.monthrange(date.year, date.month)[1]
    print(calendar.monthrange(date.year, date.month))#?
    last = date.replace(day=days)
    next = last + datetime.timedelta(days=1)
    month = str(next.year) + '-' + str(next.month)
    return month







def getCalendar(request):
    today = get_date(request.GET.get('month'))
    prev = prev_month(today)
    next = next_month(today)

    category = request.GET.get('category')
    if Category.objects.get(c_id=category).c_diary == True:
        htmlCalendar = Dalendar(today.year, today.month, category)
    else:
        htmlCalendar = Calendar(today.year, today.month, category)

    htmlCalendar.setfirstweekday(calendar.SUNDAY)
    cal = htmlCalendar.formatmonth(withyear=True)

    allCate = Category.objects.filter(c_user=request.user)

    context = {'cal': cal, 'prev_month': prev, 'next_month': next, 'category':category, 'object_list':allCate}
    return render(request, 'home.html', context=context)



def getFriendCalendar(request):
    today = get_date(request.GET.get('month'))
    prev = prev_month(today)
    next = next_month(today)

    partner = User.objects.get(username=request.GET.get('friend'))
    category = Category.objects.get(c_user=partner, c_cate=request.GET.get('category'))
    if Category.objects.get(c_cate=category, c_user = partner).c_diary == True:
        htmlCalendar = Dalendar(today.year, today.month, category.c_id)
    else:
        htmlCalendar = Calendar(today.year, today.month, category.c_id)

    htmlCalendar.setfirstweekday(calendar.SUNDAY)
    cal = htmlCalendar.formatmonth(withyear=True)

    context = {'cal': cal, 'prev_month': prev, 'next_month': next, 'category': category, 'partner': partner }
    return render(request, 'homeFriend.html', context=context)





# 카테고리
class CategoryLV(ListView):
    model = Category
    template_name = 'schedule/cate_list.html'

    def get_queryset(self):
        return Category.objects.filter(c_user = self.request.user)

class CategoryDV(DetailView):
    model = Category
    template_name = 'schedule/cate_detail.html'


class CategoryCV(CreateView):
    model = Category
    #fields = ['c_cate', 'c_star']
    template_name = 'schedule/cate_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('schedule:cateList')

    def form_valid(self, form):
        form.instance.c_user = self.request.user
        return super().form_valid(form)

    #def get_success_url(self):
    #    return reverse_lazy('schedule:cateDetail', args=(self.object.pk,))


class CategoryUV(UpdateView):
    model = Category
    #fields = ['c_cate', 'c_star']
    form_class = CategoryForm
    template_name = 'schedule/cate_update.html'
    success_url = reverse_lazy('schedule:cateList')

    def form_valid(self, form):
        form.instance.c_user = self.request.user
        return super().form_valid(form)



class CategoryDelete(DeleteView):
    model = Category
    template_name = 'schedule/cate_delete.html'
    success_url = reverse_lazy('schedule:cateList')



# 일정

#DayArchiveView
def Schedule_date(request, cate, date):
    day_list = Schedule.objects.filter(Q(s_cate=cate), Q(s_startDate = date) | Q(s_endDate = date) | Q(s_startDate__lt = date) & Q(s_endDate__gt = date) ).order_by('-s_busy')
    return render(request, 'schedule/sche_day_list.html', {'day_list':day_list, 'date':date, 'category': cate})


class ScheduleDV(DetailView):
    model = Schedule
    template_name = 'schedule/sche_detail.html'



class ScheduleCV(OwnerCategoryCheck, CreateView):
    model = Schedule
    form_class = ScheduleForm
    #fields = ['s_cate', 's_content', 's_startDate', 's_endDate', 's_red', 's_busy', 's_complete']
    template_name = 'schedule/sche_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['cate']
        context['date'] = self.kwargs['date']
        return context

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.s_user = self.request.user
        # form.cleand_date['']
        form.save()

        object_list = Category.objects.filter(c_user = self.request.user)
        return render(self.request, 'home.html', {'object_list': object_list, 'passCateId': self.kwargs['cate']})


class ScheduleUV(OwnerOnlyMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedule/sche_update.html'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.s_user = self.request.user
        form.save()

        object_list = Category.objects.filter(c_user=self.request.user)
        return render(self.request, 'home.html', {'object_list': object_list, 'passCateId': self.kwargs['cate']})


def ScheduleDel(request, pk, cate, date):
    object = Schedule.objects.get(s_id=pk)
    if object.s_user == request.user:
        object.delete()
        msg = '삭제되었습니다.'
    else:
        msg = '소유자만 접근 가능합니다.'
    return HttpResponseRedirect(reverse('schedule:scheDate', kwargs={'cate':cate, 'date':date, 'msg': msg}))





class SearchCalendar(TemplateView):
    template_name = 'schedule/search_calendar.html'

def SearchResult(request):
    if request.POST:
        search = request.POST['search_word']    # get absolute url && cate && title && date
        try:
            sche_list = Schedule.objects.filter(s_user = request.user, s_content__contains = search)
        except Schedule.DoesNotExist:
            sche_list = 'None'
        try:
            diary_list = Diary.objects.filter(Q(d_user = request.user), Q(d_title__contains = search) | Q(d_content__contains = search))
        except Diary.DoesNotExist:
            diary_list = 'None'

        return render(request, 'schedule/search_calendar.html', {'search':search, 'sche_list':sche_list, 'diary_list':diary_list})
