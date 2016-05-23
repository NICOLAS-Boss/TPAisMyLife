from django.contrib import admin
from .models import *


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2

class PostModelAdmin(admin.ModelAdmin):
    list_filter = ('author','created_date')
    inlines = [CommentInline]


class ProfileModelAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Post,PostModelAdmin)
admin.site.register(Comment)
admin.site.register(Profile,ProfileModelAdmin)
