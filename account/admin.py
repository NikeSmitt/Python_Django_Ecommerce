from django.contrib import admin

from account.models import UserBase

@admin.register(UserBase)
class UserBaseAdmin(admin.ModelAdmin):
    pass