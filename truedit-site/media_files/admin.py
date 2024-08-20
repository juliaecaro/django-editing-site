from django.contrib import admin
from embed_video.admin import AdminVideoMixin

# Register your models here.

from .models import Thumbnails, Videos
from .utils import format_count

# admin.site.register(Thumbnails)
# admin.site.register(Videos)

class LikesFilter(admin.SimpleListFilter):
    title = 'likes'
    parameter_name = 'likes_range'

    def lookups(self, request, model_admin):
        # Get the range values from the database
        queryset = model_admin.model.objects.all()

        ranges = {
            '0-999': 'Less than 1K',
            '1000-4999': '1K - 5K',
            '5000-9999': '5K - 10K',
            '10000-99999': '10K - 100K',
            '100000+': '100K+',
            '500000+': '500K+',
        }

        # Check which ranges have records
        available_ranges = {}
        for key, label in ranges.items():
            if self.range_exists(queryset, key):
                available_ranges[key] = label

        return [(key, label) for key, label in available_ranges.items()]

    def range_exists(self, queryset, key):
        if key == '0-999':
            return queryset.filter(likes__lt=1000).exists()
        elif key == '1000-4999':
            return queryset.filter(likes__gte=1000, likes__lt=5000).exists()
        elif key == '5000-9999':
            return queryset.filter(likes__gte=5000, likes__lt=10000).exists()
        elif key == '10000-99999':
            return queryset.filter(likes__gte=10000, likes__lt=100000).exists()
        elif key == '100000-499999':
            return queryset.filter(likes__gte=100000, likes__lt=500000).exists()
        elif key == '500000+':
            return queryset.filter(likes__gte=500000).exists()
        return False

    def queryset(self, request, queryset):
        value = self.value()
        if value == '0-999':
            return queryset.filter(likes__lt=1000)
        elif value == '1000-4999':
            return queryset.filter(likes__gte=1000, likes__lt=5000)
        elif value == '5000-9999':
            return queryset.filter(likes__gte=5000, likes__lt=10000)
        elif value == '10000+':
            return queryset.filter(likes__gte=10000)
        elif value == '100000+':
            return queryset.filter(likes__gte=100000)
        elif value == '500000+':
            return queryset.filter(likes__gte=500000)
        return queryset

class ViewsFilter(admin.SimpleListFilter):
    title = 'views'
    parameter_name = 'views_range'

    def lookups(self, request, model_admin):
        # Get the range values from the database
        queryset = model_admin.model.objects.all()
        ranges = {
            '0-999': 'Less than 1K',
            '1000-4999': '1K - 5K',
            '5000-9999': '5K - 10K',
            '10000-99999': '10K - 100K',
            '100000+': '100K+',
            '500000+': '500K+',
        }

        # Check which ranges have records
        available_ranges = {}
        for key, label in ranges.items():
            if self.range_exists(queryset, key):
                available_ranges[key] = label

        return [(key, label) for key, label in available_ranges.items()]

    def range_exists(self, queryset, key):
        if key == '0-999':
            return queryset.filter(views__lt=1000).exists()
        elif key == '1000-4999':
            return queryset.filter(views__gte=1000, views__lt=5000).exists()
        elif key == '5000-9999':
            return queryset.filter(views__gte=5000, views__lt=10000).exists()
        elif key == '10000-99999':
            return queryset.filter(views__gte=10000, views__lt=100000).exists()
        elif key == '100000-499999':
            return queryset.filter(views__gte=100000, views__lt=500000).exists()
        elif key == '500000+':
            return queryset.filter(views__gte=500000).exists()
        return False

    def queryset(self, request, queryset):
        value = self.value()
        if value == '0-999':
            return queryset.filter(views__lt=1000)
        elif value == '1000-4999':
            return queryset.filter(views__gte=1000, views__lt=5000)
        elif value == '5000-9999':
            return queryset.filter(views__gte=5000, views__lt=10000)
        elif value == '10000+':
            return queryset.filter(views__gte=10000)
        elif value == '100000+':
            return queryset.filter(likes__gte=100000)
        elif value == '500000+':
            return queryset.filter(likes__gte=500000)
        return queryset

# Define the admin class
class ThumbnailsAdmin(admin.ModelAdmin):
    list_display = ('truncated_title', 'language', 'truncated_game', 'date_uploaded')
    list_filter = ('language', 'game', 'date_uploaded')

    fieldsets = (
      (None, {
          'fields': ('title', 'image', 'language',)
      }),
      ('Other information', {
          'fields': ('game', 'date_uploaded')
      }),
)

    def truncated_title(self, obj):
        return obj.truncated_title
    truncated_title.short_description = 'Title'
    truncated_title.admin_order_field = 'title'  # Enable sorting by titles

    def truncated_game(self, obj):
        return obj.truncated_game
    truncated_game.short_description = 'Game'
    truncated_game.admin_order_field = 'game'  # Enable sorting by games

# Define the admin class
class VideosAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ('truncated_title', 'language', 'client', 'formatted_likes', 'formatted_views', 'truncated_game', 'date_uploaded')
    list_filter = ('language', 'client', LikesFilter, ViewsFilter, 'game', 'date_uploaded')

    fieldsets = (
      (None, {
          'fields': ('title', 'video', 'language', 'likes', 'views')
      }),
      ('Other information', {
          'fields': ('client', 'game', 'date_uploaded')
      }),
)

    def truncated_title(self, obj):
        return obj.truncated_title
    truncated_title.short_description = 'Title'
    truncated_title.admin_order_field = 'title'  # Enable sorting by titles

    def truncated_game(self, obj):
        return obj.truncated_game
    truncated_game.short_description = 'Game'
    truncated_game.admin_order_field = 'game'  # Enable sorting by games

    def formatted_likes(self, obj):
        return format_count(obj.likes)
    formatted_likes.short_description = 'Likes'
    formatted_likes.admin_order_field = 'likes'  # Enable sorting by likes

    def formatted_views(self, obj):
        return format_count(obj.views)
    formatted_views.short_description = 'Views'
    formatted_views.admin_order_field = 'views'  # Enable sorting by views

# Register the admin class with the associated model
admin.site.register(Thumbnails, ThumbnailsAdmin)
admin.site.register(Videos, VideosAdmin)