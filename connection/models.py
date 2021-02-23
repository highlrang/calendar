from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from schedule.models import Category

# Create your models here.
class Friends(models.Model): # 친구 목록에서 사용할 테이블
    f_id = models.AutoField(primary_key = True)
    f_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    f_partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partner')
    f_cate = models.ForeignKey(Category, on_delete=models.CASCADE, null=True) # 상대의 카테고리 저장하기 !!!!

    class Meta:
        ordering = ['f_user', 'f_id']

    def __str__(self):
        return self.f_user

class Proposal(models.Model): # 친구 신청에서 수락 과정에서 사용할 테이블
    p_id = models.AutoField(primary_key=True)
    p_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myname')
    p_partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='yourname')
    p_cate = models.ForeignKey(Category, on_delete=models.CASCADE, null=True) # user(my) cate
    p_reject = models.BooleanField(default=False)

