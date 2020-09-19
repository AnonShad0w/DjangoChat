from django.contrib import admin

from .models import Room

class RoomAdmin(admin.ModelAdmin):
	fields = ['title']

admin.site.register(Room, RoomAdmin)
