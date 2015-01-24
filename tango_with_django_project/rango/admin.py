from django.contrib import admin
from rango.models import Category, Page


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(model_or_iterable=Category, admin_class=CategoryAdmin)


class PageAdmin(admin.ModelAdmin):
    fields = ["category", "title", "url", "views"]
    list_display = ("title", "category", "url")
    list_filter = ['category']

admin.site.register(model_or_iterable=Page, admin_class=PageAdmin)