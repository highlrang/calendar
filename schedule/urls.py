from django.urls import path, include
from .views import *

app_name = 'schedule'
urlpatterns = [
    path('calendar/', getCalendar, name='getCalendar'),
    path('calendar/friend/', getFriendCalendar, name='getFriendCalendar'),

    path('category/', CategoryLV.as_view(), name='cateList'),
    path('category/<int:pk>/', CategoryDV.as_view(), name='cateDetail'),
    path('category/create/', CategoryCV.as_view(), name='cateCreate'),
    path('category/update/<int:pk>/', CategoryUV.as_view(), name='cateUpdate'),
    path('category/delete/<int:pk>/', CategoryDelete.as_view(), name='cateDelete'),

    path('<int:cate>/<str:date>/', Schedule_date, name='scheDate'),
    path('<int:pk>/', ScheduleDV.as_view(), name='scheDetail'),
    path('create/<int:cate>/<str:date>/', ScheduleCV.as_view(), name='scheCreate'),
    path('update/<int:pk>/<int:cate>/<str:date>/', ScheduleUV.as_view(), name='scheUpdate'),
    path('delete/<int:pk>/<int:cate>/<str:date>/', ScheduleDel, name='scheDelete'),

]