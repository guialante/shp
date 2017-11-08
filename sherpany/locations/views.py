from django.views.generic import View, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import IntegrityError

from braces import views
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from .models import Location


class LocationListView(ListView):
    model = Location
    template_name = 'pages/home.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(LocationListView, self).dispatch(*args, **kwargs)
    

class FusionTablesMixin(object):
    """
        This mixin is in charge to create the connection via API google fusion tables.
    """
    table_id = '18rhJFN48wNEtoQ3mHO4ePlbxaH0hRS8TBH48WBxX'
    
    def connect_google_api(self):
        scopes = ['https://www.googleapis.com/auth/fusiontables']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('test-5a8d161cf91c.json', scopes)
        fusion_tables = build('fusiontables', 'v2', credentials=credentials)
        return fusion_tables
    
    def insert_record(self, address, lat, lng):
        fusion_tables = self.connect_google_api()
        sql = "INSERT INTO {} (address, location) VALUES ('{}', '{},{}')".format(
            self.table_id, address, lat, lng
        )
        obj = fusion_tables.query().sql(sql=sql).execute()
        return obj
        
    def delete_records(self):
        fusion_tables = self.connect_google_api()
        sql = "DELETE FROM {}".format(self.table_id)
        obj = fusion_tables.query().sql(sql=sql).execute()
        return obj
    

class SaveLocationAjaxView(FusionTablesMixin, views.JSONResponseMixin, views.AjaxResponseMixin, View):
    """
        This view is in charge of create addresses on the database and the fusion table as well
    """
    require_json = True

    def post_ajax(self, request, *args, **kwargs):
        address = request.POST.get('address')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')

        if address and lat and lng:
            try:
                instance = Location.objects.create(address=address, lat=lat, lng=lng)
            except IntegrityError:
                instance = None
            
            if instance is not None:
                self.insert_record(address, lat, lng)
        
        json_dict = {
            'address': address,
            'created': True
        }
        return self.render_json_response(json_dict)


class DeleteLocationsAjaxView(FusionTablesMixin, views.JSONResponseMixin, views.AjaxResponseMixin, View):
    """
        This view is in charge of delete addresses on the database and the fusion table as well
    """
    require_json = True
    
    def post_ajax(self, request, *args, **kwargs):
        is_delete = request.POST.get('delete')
        
        if is_delete:
            Location.objects.all().delete()
            self.delete_records()
        
        json_dict = {
            
            'delete': True
        }
        return self.render_json_response(json_dict)
