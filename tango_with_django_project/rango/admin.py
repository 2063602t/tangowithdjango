from django.contrib import admin
from rango.models import Category, Page

# Register your models here.
admin.site.register(model_or_iterable=Category)


class PageAdmin(admin.ModelAdmin):
    fields = ["category", "title", "url", "views"]
    list_display = ("title", "category", "url")


admin.site.register(model_or_iterable=Page, admin_class=PageAdmin)