from django.contrib import admin
from .models import *
# Register your models here.



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('c_id', 'c_user', 'c_cate', 'c_star', 'c_diary')
    list_filter = ['c_user', 'c_star']
    #fields = [] 추가??
    search_fields = ['c_user']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('s_id', 's_user', 'cate_name', 's_content', 's_startDate', 's_endDate', 's_busy', 's_red', 's_complete')
    list_filter = ['s_cate', 's_red', 's_busy', 's_complete']
    fields = ['s_user', 's_cate', 's_content', ('s_startDate', 's_endDate'), 's_busy', ('s_red', 's_complete')]
    search_fields = ['s_user', 's_cate']

    #date_hierarchy =
    #fieldsets = ()

    def cate_name(self, obj):
        return obj.s_cate.c_cate

    cate_name.admin_order_field = 'cate_name'
    cate_name.short_description = 'cate_name'

# admin.StackedInline > inlines = [MakedInline]
# actions = [] 도 가능!


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('d_id', 'd_user', 'cate_name', 'd_title')
    list_filter = ['d_user', 'd_cate']
    search_fields = ['d_user', 'd_cate']

    def cate_name(self, obj):
        return obj.d_cate.c_cate

    cate_name.admin_order_field = 'cate_name'
    cate_name.short_description = 'cate_name'