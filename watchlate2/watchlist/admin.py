from django.contrib import admin

from .models import WatchList, PlatformStream, Review

# Register your models here.

admin.site.register(WatchList)
admin.site.register(PlatformStream)
admin.site.register(Review)
