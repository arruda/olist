from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^api/', include('sales_channels.api.urls')),
    url(r'^admin/', admin.site.urls),
]
