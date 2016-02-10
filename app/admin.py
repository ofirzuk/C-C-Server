from django.contrib import admin
from .models import Data, Malware, Command, File
# Register your models here.

admin.site.register(Data)
admin.site.register(Command)
admin.site.register(Malware)
admin.site.register(File)