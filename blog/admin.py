from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

admin.sites.AdminSite.site_header = "پنل مدیریت"
admin.sites.AdminSite.site_title = "پنل"
admin.sites.AdminSite.index_title = "سایت آریرانگلند"


# Inlines

class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0



# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status']
    ordering = ['publish']
    list_filter = ['author', 'status', ('publish', JDateFieldListFilter)]
    search_fields = ['description']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['status']
    list_display_links = ['author', 'title']
    inlines = [ImageInline, CommentInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created', 'active']
    list_filter = ['active', ('created', JDateFieldListFilter)]
    search_fields = ['name', 'post', 'text']
    list_editable = ['active']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'created']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'bio', 'job', 'photo']
