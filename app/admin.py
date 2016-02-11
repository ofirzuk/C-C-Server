from django.contrib import admin
from .models import DataItem, Malware, Command, File
# Register your models here.

admin.site.register(DataItem)
admin.site.register(Command)
admin.site.register(Malware)
admin.site.register(File)