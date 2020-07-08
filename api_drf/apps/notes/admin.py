from django.contrib import admin

from .models import Note


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['note', 'user', 'first_name', 'last_name']

admin.site.register(Note)
# admin.site.register(Profile, ProfileAdmin)
