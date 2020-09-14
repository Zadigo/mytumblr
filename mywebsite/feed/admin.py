from django.contrib import admin
from feed import models

@admin.register(models.Video)
class TimeLineAdmin(admin.ModelAdmin):
    list_display = ['reference', 'views', 'reports', 'reported', 'visible']
    search_fields = ['user__username', 'reference']
    filter_horizontal = ['tags']
    date_hierarchy = 'created_on'
    list_per_page = 30 


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'comment']
    list_per_page = 30 


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'video']
    date_hierarchy = 'created_on'
    list_per_page = 30 


@admin.register(models.Search)
class SearchesAdmin(admin.ModelAdmin):
    list_display = ['user', 'term']
    search_fields = ['user__username', 'term']
    date_hierarchy = 'created_on'
    list_per_page = 30
