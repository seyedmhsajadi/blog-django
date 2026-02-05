from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


# Register your models here.
'''کد های شخصی سازی دستی زبان پنل مدیریت جنگو 
بدون استفاده از تغییر زبان خودکار جنگو از طریق setting.py'''
#admin.sites.AdminSite.site_header = "پنل مدیریت جنگو"
#admin.sites.AdminSite.site_title = "پنل"
#admin.sites.AdminSite.index_title = "پنل مدیریت"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'publish']
    ordering = ['title', 'publish']
    list_filter = ['status', 'author', ('publish', JDateFieldListFilter)]
    search_fields = ['title']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    #list_display_links = ['author']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created', 'active']
    list_filter = ['active']
    search_fields = ['name', 'body']
    list_editable = ['active']