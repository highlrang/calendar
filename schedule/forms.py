from django import forms
from django.forms import fields
from .models import Category, Schedule
from .widgets import FCDatePickerWidget
from django.contrib.admin import widgets # AdminDateWidget

# parent_model & validation

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['c_cate', 'c_star', 'c_diary']
        labels = {
            "c_cate": "카테고리",
            "c_diary": "다이어리",
            "c_star" : "즐겨찾기"

        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['s_cate', 's_content', 's_startDate', 's_endDate', 's_busy', 's_red', 's_complete']
        widgets = {
            "s_startDate" : FCDatePickerWidget,
            "s_endDate" : FCDatePickerWidget

        }
        labels = {
            "s_cate" : "카테고리",
            "s_content" : "일정 내용",
            "s_startDate" : "시작일",
            "s_endDate" : "종료일",
            "s_busy" : "중요도",
            "s_red" : "기념일",
            "s_complete" : "완료"
        }