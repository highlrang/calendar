from django.urls import path
from .views import *

app_name = 'diary'
urlpatterns = [
    path('<int:cate>/<str:date>/', Diary_date, name='diaryDate'),
    path('<int:pk>/', DiaryDV.as_view(), name='diaryDetail'),
    path('create/<int:cate>/<str:date>/', DiaryCV.as_view(), name='diaryCreate'),
    path('update/<int:pk>/<int:cate>/<str:date>/', DiaryUV.as_view(), name='diaryUpdate'),
    path('delete/<int:pk>/<int:cate>/<str:date>/', DiaryDel, name='diaryDelete'),
]



