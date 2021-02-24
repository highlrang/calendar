# 캘린더 웹 프로젝트 주요 코드
+ 해당 프로젝트의 주요 기능은 일정 관리, 일기, 캘린더 공유 등 입니다.
+ 이 중에서 **일정 관리**를 중심으로 코드를 살펴보겠습니다.
+ 주석을 중심으로 살펴봐주세요.

---------------------------------------

## models.py
https://github.com/highlrang/calendar/blob/master/schedule/models.py

+ 달력의 종류를 구분하는 Category 모델과 각 달력에 종속되어 추가되는 일정들을 관리하는 Schedule 모델 생성


```python
class Category(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_user = models.ForeignKey(User, on_delete=models.CASCADE) 
    c_cate = models.CharField(max_length=30)                
    c_star = models.BooleanField(default=False)              # 즐겨찾기로 달력 우선순위 반영
    c_diary = models.BooleanField(default=False)             # 일정인지 일기인지 구분

    class Meta:
        ordering = ['c_user', '-c_id']                       # 사용자 중심으로 달력을 우선 정렬

    def __str__(self):
        return self.c_cate
        
    def get_absolute_url(self):
        return reverse('schedule:cateDetail', args=[self.c_id])

BUSY_CHOICES = (
    ('0', ''),
    ('1', '★'),
    ('2', '★★'),
    ('3', '★★★'),
    ('4', '★★★★'),
    ('5', '★★★★★')
)

class Schedule(models.Model):
    s_id = models.AutoField(primary_key=True)                                                     # primary_key 생성
    s_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)                         # 사용자에 종속
    s_cate = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)                     # 카테고리 지정(상위 모델)
    s_content = models.CharField(max_length=200)                                                  # 일정 내용
    s_startDate = models.DateField(null=True)                                                     # 시작 날짜 지정    
    s_endDate = models.DateField(null=True)                                              
    s_red = models.BooleanField(default=False)                                                    # 기념일 여부
    s_busy = models.CharField(max_length=1, choices=BUSY_CHOICES, default=BUSY_CHOICES[0][0])     # 중요도 여부 - choices 사용
    s_complete = models.BooleanField(default=False)                                               # 완료 여부

    class Meta:
        ordering = ['s_cate', '-s_id']                                       # 일정은 가장 근접한 상위 모델인 카테고리끼리 정렬하기

    def __str__(self):
        return self.s_content

    def get_absolute_url(self):
        return reverse('schedule:scheDetail', args=[self.s_id])
```
----------------------------------------
## urls.py
https://github.com/highlrang/calendar/blob/master/schedule/urls.py

```python
from django.urls import path, include
from .views import *

app_name = 'schedule'
urlpatterns = [

# 달력 소환 url
    path('calendar/', getCalendar, name='getCalendar'),
    path('calendar/friend/', getFriendCalendar, name='getFriendCalendar'),

# 카테고리 url
    path('category/', CategoryLV.as_view(), name='cateList'),
    path('category/<int:pk>/', CategoryDV.as_view(), name='cateDetail'),
    path('category/create/', CategoryCV.as_view(), name='cateCreate'),
    path('category/update/<int:pk>/', CategoryUV.as_view(), name='cateUpdate'),
    path('category/delete/<int:pk>/', CategoryDelete.as_view(), name='cateDelete'),

# 일정 url
    path('<int:cate>/<str:date>/', Schedule_date, name='scheDate'),                                 # 일정 day를 기준으로 archive
    path('<int:pk>/', ScheduleDV.as_view(), name='scheDetail'),                                     # 일정 디테일뷰
    path('create/<int:cate>/<str:date>/', ScheduleCV.as_view(), name='scheCreate'),                 # 일정 생성뷰
    path('update/<int:pk>/<int:cate>/<str:date>/', ScheduleUV.as_view(), name='scheUpdate'),        # 일정 업데이트뷰
    path('delete/<int:pk>/<int:cate>/<str:date>/', ScheduleDel, name='scheDelete'),                 # 일정 삭제

# 일정 검색 url
    path('search/', SearchCalendar.as_view(), name='searchCalendar'),
    path('search/result/', SearchResult, name='searchResult'),
]
```


----------------------------------------
## views.py
https://github.com/highlrang/calendar/blob/master/schedule/views.py

1. 캘린더 호출 코드 - HTMLCalendar 재정의하는 코드는 인터넷을 참고하였고, 모델을 다루는 부분은 전부 새로 

```python

 # HTMLCalendar를 재정의 >> Category를 넘겨받아 해당 카테고리의 일정들을 날짜에 맞춰 삽입
class Calendar(HTMLCalendar):                                                          
    def __init__(self, year=None, month=None, category=None):
        self.year = year
        self.month = month
        self.category = category
        super(Calendar, self).__init__()

    def formatday(self, day):
        todo_list = ''

        if day != 0:
            date = datetime.date(self.year, self.month, day)
# Q조건문을 활용하여 해당하는 일정 데이터가 존재한다면, 중요도를 다루는 필드를 기준으로 내림차순하여 변수에 담는다.
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
# 완료여부 확인
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
# 각 날짜에 date archive 페이지로 가는 url담기 + 각 날짜에 해당하는 일정들 담기
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
        
        
        
# 전달받은 날짜 format해서 전달    
def get_date(date):
    if date:
        year, month = (int(i) for i in date.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

# 이전달 다음달 반환 
def prev_month(date):
    first = date.replace(day=1)
    prev = first - datetime.timedelta(days=1)
    month = str(prev.year) + '-' + str(prev.month)
    return month

def next_month(date):
    days = calendar.monthrange(date.year, date.month)[1]
    last = date.replace(day=days)
    next = last + datetime.timedelta(days=1)
    month = str(next.year) + '-' + str(next.month)
    return month


# 달력 소환 함수
def getCalendar(request):
    today = get_date(request.GET.get('month'))
    prev = prev_month(today)
    next = next_month(today)

    category = request.GET.get('category')
# 다이어리 여부 확인
    if Category.objects.get(c_id=category).c_diary == True:
        htmlCalendar = Dalendar(today.year, today.month, category)
    else:
# Calendar 클래스 호출해서 전달할 달력 생성 - 요청한 년도, 월에 해당하는 일정들이 담겨져 전달됨
        htmlCalendar = Calendar(today.year, today.month, category)

    htmlCalendar.setfirstweekday(calendar.SUNDAY)
    cal = htmlCalendar.formatmonth(withyear=True)

# 사용자의 카테고리 리스트 전달 
    allCate = Category.objects.filter(c_user=request.user)

    context = {'cal': cal, 'prev_month': prev, 'next_month': next, 'category':category, 'object_list':allCate}
    return render(request, 'home.html', context=context)
```



---------------------------------------------------------------------------------------------------------------------------------------



2. 일정 호출 코드
```python


# day archive 뷰 - 날짜가 start와 end 사이에 걸려있는 일정이 있어 generic 클래스형 뷰가 아닌 def 함수로 선택
# Q 조건문과 ORM 필드 값에 대한 option을 이용하여 요청받은 날짜에 속해있는 일정들을 반환

def Schedule_date(request, cate, date):
    day_list = Schedule.objects.filter(Q(s_cate=cate), Q(s_startDate = date) | Q(s_endDate = date) | Q(s_startDate__lt = date) & Q(s_endDate__gt = date) ).order_by('-s_busy')
    return render(request, 'schedule/sche_day_list.html', {'day_list':day_list, 'date':date, 'category': cate})




# 일정 CreateView 간단히 살펴보기
# 친구 달력도 볼 수 있기 때문에 CreateView, UpdateView, delete의 경우 소유자가 아니면 접근할 수 없게 설정
# 아래의 CreateView에서는 OwnerCategoryCheck함수 사용(https://github.com/highlrang/calendar/blob/master/mysite/views.py)에 코드 있음

class ScheduleCV(OwnerCategoryCheck, CreateView):
    model = Schedule
# 전용 form 생성 (https://github.com/highlrang/calendar/blob/master/schedule/forms.py)
    form_class = ScheduleForm          
# 사용자에게 보여질 template
    template_name = 'schedule/sche_create.html'                                                       


# context 변수 - 카테고리와 날짜 정보 전달
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['cate']                                                     
        context['date'] = self.kwargs['date']
        return context


# 데이터 생성하기 전에 빈 값으로 설정된 일정 소유자(s_user) 지정한 후 저장
    def form_valid(self, form):                                                                        
        form.save(commit=False)
        form.instance.s_user = self.request.user
        form.save()

        object_list = Category.objects.filter(c_user = self.request.user)                                         
        return render(self.request, 'home.html', {'object_list': object_list, 'passCateId': self.kwargs['cate']})

```

----------------------------------------

## templates

1. 홈페이지
https://github.com/highlrang/calendar/blob/master/templates/home.html

```html
{% extends 'base.html' %}
{% load static %}
{% block content %}
    {% if user.is_active %}

# 카테고리 즐겨찾기 되어 있는 것을 앞에 위치시킴 - object_list가 카테고리 리스트

        {% for i in object_list %}
            {% if i.c_star == True %} <!-- queryset order by로도 가능 -->
            <span><input type="button" class="cate" onclick="location.href='{% url 'schedule:getCalendar' %}?category={{ i.c_id }}'" id="{{ i.c_id }}" value="{{ i.c_cate }}" /></span>
            {% endif %}
        {% endfor %}

        {% for i in object_list %}
            {% if i.c_star == False %}
            <span><input type="button" class="cate" onclick="location.href='{% url 'schedule:getCalendar' %}?category={{ i.c_id }}'" id="{{ i.c_id }}" value="{{ i.c_cate }}" /></span>
            {% endif %}
        {% endfor %}

        <br><br>
        {% if cal %}
        <div style="clear: both;">
            <div style="float: left;">
            
# 이전달, 다음달 전달받은 변수를 담아서 해당 년월에 해당하는 달력 호출하는(getCalendar) url 생성
                <input type="button" onclick="location.href='{% url 'schedule:getCalendar' %}?month={{ prev_month }}&category={{ category }}'" value="이전 달"/>
            </div>
            <div style="float: right;">
                <input type="button" onclick="location.href='{% url 'schedule:getCalendar' %}?month={{ next_month }}&category={{ category }}'" value="다음 달"/>
            </div>
        </div>
        {% else %}
# 카테고리가 없을 경우
        <p>카테고리를 생성한 후 캘린더를 이용하세요!</p>
        {% endif %}

        <div>
        {% autoescape off %}
# 달력
              {{ cal }}
        {% endautoescape %}
        </div>

    {% else %}
# 로그인이 안 되어 있을 겨웅
    <br>
        <div style="text-align: center;">
            <p> 로그인 또는 간단한 회원가입으로 앱 사용을 시작해보세요 !</p><br>
            <div><input type="button" onclick="location.href='{% url 'login' %}'" value="로그인"/></div><br>
            <div><input type="button" onclick="location.href='{% url 'register' %}'" value="회원가입"/></div><br>
        </div>
    {% endif %}


{% endblock %}


```


---------------------------------------------------------



2. 각 날짜에 속해있는 일정들 리스트를 반환하는 template (day_archive_view)
https://github.com/highlrang/calendar/blob/master/schedule/templates/schedule/sche_day_list.html


```python
{% extends 'base.html' %}
{% block content %}
    <script>
# 삭제 기능 시 전달받은 메세지 파라미터를 alert로 화면에 띄우기
        $(function(){
            if ("{{ msg }}" != ""):
                alert("{{ msg }}");
        });

# 삭제 버튼 클릭 시 한 번 더 확인하고 url 이동
        function checkDelete(id){
            var answer = confirm("삭제하시겠습니까");
            if(answer){
                location.href="/schedule/delete/"+id+"/{{ category }}/{{ date }}/";
            }
        }

    </script>
    <br>
    
      {{ date }}의 일정 &ensp;&ensp;&ensp;
 # 일정 추가 url
      <input type="button" onclick="location.href='{% url 'schedule:scheCreate' cate=category date=date %}'" value="+ 추가"/>
      <br><br><br>

      {% if day_list %}
      <div style="border-radius: 10px; border-left: 1px solid black; border-right: 1px solid black; padding: 3%;">
# 해당 날짜의 각 일정들 for문으로 출력
       {% for i in day_list %}
          <div>
# detail view로 이동하는 url - get_absolute_url 이용
              <span style="display: inline-block; width: 40%;"><a href="{{ i.get_absolute_url }}">{{ i.s_content }}</a></span>
# 삭제는 html 버튼 클릭 시 javascript 함수로 이동하여 url 이동하는 구조
              <span style="display: inline-block; width: 10%;"><input type="button" onclick="checkDelete({{ i.s_id }})" value="삭제"/></span>
# 일정 update view로 이동하는 url - get 방식으로 필요한 파라미터 전달
              <span style="display: inline-block; width: 10%;"><input type="button" onclick="location.href='{% url 'schedule:scheUpdate' pk=i.s_id cate=category date=date %}'" value="수정"/></span>
          </div><br>
      {% endfor %}
      </div>
      {% endif %}
{% endblock %}
```
