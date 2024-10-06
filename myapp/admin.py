from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(file_uplode)
admin.site.register(folders)
admin.site.register(profiles)
admin.site.register(messages)
admin.site.register(CustomUser, UserAdmin)
