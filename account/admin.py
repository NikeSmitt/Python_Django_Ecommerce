from django.contrib import admin

from account.models import Customer, Address


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Address)
