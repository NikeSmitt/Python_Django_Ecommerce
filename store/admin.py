from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (Category, Product, ProductImage, ProductType, ProductSpecification, ProductSpecificationValue)

admin.site.register(Category, MPTTModelAdmin)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline
    ]

class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]
    list_filter = ['is_active']
    list_editable = []
    prepopulated_fields = {'slug': ('title',)}
