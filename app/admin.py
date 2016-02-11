from django.contrib import admin
from .models import DataItem, Malware, Command, FileItem


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_filter = ('malware',)
    list_display = ('type', 'value', 'malware', 'timestamp')


@admin.register(DataItem)
class DataItemAdmin(admin.ModelAdmin):
    list_filter = ('malware',)
    list_display = ('name', 'data', 'malware')


@admin.register(FileItem)
class FileAdmin(admin.ModelAdmin):
    list_filter = ('malware',)
    list_display = ('name', 'data', 'malware')


@admin.register(Malware)
class MalewareAdmin(admin.ModelAdmin):
    list_display = ('teammates', 'token')
