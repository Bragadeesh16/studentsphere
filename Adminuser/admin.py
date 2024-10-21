from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(file_uplode)
admin.site.register(folders)