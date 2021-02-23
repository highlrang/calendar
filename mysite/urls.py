"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from mysite.views import *

from django.conf.urls import handler400, handler403, handler404, handler500
"""
handler400 = 'mysite.views.bad_request'
handler403 = 'mysite.views.permission_denied'
handler404 = 'mysite.views.page_not_found'
handler500 = 'mysite.views.server_error'
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('<int:cate>/', Before_Home, name='before_home'),

    path('accounts/', include('django.contrib.auth.urls')), # 로그인
    path('accounts/register/', UserCreateView.as_view(), name='register'), #회원가입
    path('accounts/register/done/', UserCreateDoneTV.as_view(), name='register_done'), #회원가입
    path('accounts/signOut/', UserSignOut.as_view(), name='sign_out'),
    path('accounts/signOut/done/', UserSignOut_done, name='sign_out_done'), # 탈퇴
    path('settings/', user_settings.as_view(), name='settings'),

    path('schedule/', include('schedule.urls')),
    path('diary/', include('diary.urls')),
    path('connection/', include('connection.urls')),
]
