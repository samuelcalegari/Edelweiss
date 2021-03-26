from django.contrib import admin
from .models import *

# Disable delete from list
admin.site.disable_action('delete_selected')

# Register your models here.

# Points Of Interest
class PointsOfInterestInline(admin.TabularInline):
    model = PointsOfInterest
    extra = 0
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

# Hikes
class HikeAdmin(admin.ModelAdmin):
    list_display = ('title', 'note', 'thumbnail_preview')
    readonly_fields = ('thumbnail_preview',)

    @staticmethod
    def note(obj):
        return obj.note

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True
    inlines = [
        PointsOfInterestInline,
    ]

admin.site.register(Hike, HikeAdmin)

# Badges
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('title','thumbnail_preview')
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True

admin.site.register(Badge, BadgeAdmin)


# UserHike
class UserHikeAdmin(admin.ModelAdmin):
    list_display = ('user','hike')

admin.site.register(UserHike, UserHikeAdmin)


# UserBadge
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user','badge')

admin.site.register(UserBadge, UserBadgeAdmin)

