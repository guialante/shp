"""sherpany URL Configuration

"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static

from sherpany.locations.views import LocationListView, SaveLocationAjaxView, DeleteLocationsAjaxView


urlpatterns = [
    url(r'^$', LocationListView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^save-location/$', SaveLocationAjaxView.as_view(), name='save_location'),
    url(r'^delete-locations/$', DeleteLocationsAjaxView.as_view(), name='delete_locations'),
    url(r'^admin/', admin.site.urls),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
