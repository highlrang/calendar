from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# 일정 저장하는 모델
class Category(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_user = models.ForeignKey(User, on_delete=models.CASCADE) # 탈퇴 시 없어지는 것 안내 + 탈퇴하시겠습니까 alert
    c_cate = models.CharField(max_length=30)
    c_star = models.BooleanField(default=False)              #즐겨찾기 True면 상단에
    c_diary = models.BooleanField(default=False)

    class Meta:
        # verbose_name =
        ordering = ['c_user', '-c_id']

    def __str__(self):
        return self.c_cate

    #def save():
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
    s_id = models.AutoField(primary_key=True)
    s_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    s_cate = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    s_content = models.CharField(max_length=200)
    s_startDate = models.DateField(null=True)
    s_endDate = models.DateField(null=True)  # 설정 안 할 경우 startDate로                                                # option에 auto_now=True있음
    s_red = models.BooleanField(default=False) #기념일
    s_busy = models.CharField(max_length=1, choices=BUSY_CHOICES, default=BUSY_CHOICES[0][0])
    s_complete = models.BooleanField(default=False)

    class Meta:
        ordering = ['s_cate', '-s_id']

    def __str__(self):
        return self.s_content

    def get_absolute_url(self):
        return reverse('schedule:scheDetail', args=[self.s_id])


class Diary(models.Model): # textfield
    d_id = models.AutoField(primary_key=True)
    d_user = models.ForeignKey(User, on_delete=models.CASCADE)
    d_cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    d_title = models.CharField(max_length=100)
    d_content = models.TextField()
    d_date = models.DateField()

    class Meta:
        ordering = ['d_cate', '-d_id']

    def __str__(self):
        return self.d_title

    def get_absolute_url(self):
        return reverse('diary:diaryDetail', args=[self.d_id])
