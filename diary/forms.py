from django import forms
from django.forms import fields
from schedule.models import Diary
from schedule.widgets import FCDatePickerWidget
from django.contrib.admin import widgets # AdminDateWidget

# parent_model & validation
class DiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)
        # self.fields['d_cate'].disabled = True

    class Meta:
        model = Diary
        fields = ['d_cate', 'd_date', 'd_title', 'd_content']
        widgets = {
            "d_date" : FCDatePickerWidget,

        }
        labels = {
            "d_cate" : "카테고리",
            "d_date" : "날짜",
            "d_title" : "제목",
            "d_content" : "내용",
        }