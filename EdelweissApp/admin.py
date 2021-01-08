from django.contrib import admin
from .models import *

# Register your models here.

# Hikes

class HikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','thumbnail_preview')
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True


admin.site.register(Hike, HikeAdmin)