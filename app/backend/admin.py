from django.contrib import admin
from backend.models import BotUser, Books, Template
# Register your models here.


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'chat_id']

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'type']
