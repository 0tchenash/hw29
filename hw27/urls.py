"""hw27 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from ads.views import *
from rest_framework import routers
from users.views import LocationViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('api-auth/', include('rest_framework.urls')),
    path('ads/', include('ads.urls')),
    path('user/', include('users.urls'))
    # path('location/', include('users.urls'))

#     path('cat/<int:cid>/', get_cats_by_id),
#     path('ads/', get_ads),
#     path('ads/<int:aid>/', get_ads_by_id)
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = routers.SimpleRouter()
router.register('location', LocationViewSet)
urlpatterns += router.urls
