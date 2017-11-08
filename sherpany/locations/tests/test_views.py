from django.test import RequestFactory, Client

from test_plus.test import TestCase

from ..views import SaveLocationAjaxView, DeleteLocationsAjaxView


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
    

class TestSaveLocationAjaxView(BaseUserTestCase):

    def test_post_ajax(self):
        data = {
            'address': 'Cl. 25 #31-1 a 31-67, Cali, Valle del Cauca, Colombia',
            'lat': '3.4263858',
            'lng': '-76.52020010000001'
        }
        request = self.factory.post('/save-location/', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = SaveLocationAjaxView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestDeleteLocationsAjaxView(BaseUserTestCase):

    def test_post_ajax(self):
        data = {
            'delete': True
        }
        request = self.factory.post('/delete-locations/', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = DeleteLocationsAjaxView.as_view()(request)
        self.assertEqual(response.status_code, 200)
