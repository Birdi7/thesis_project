# Create your views here.
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views import View

from thesis.models import Order
from thesis.utils.client_creator import ClientCreator


class IndexView(TemplateView):
    template_name = "index.html"


class CreateOrderView(View):
    def post(self, request: WSGIRequest):
        # TODO: test with all utm labels
        client = ClientCreator.from_order_request(request)
        
        _order = Order.objects.create(
            client=client
        )

        return JsonResponse({"status": "OK"}, status=200)


class CallibriView(View):
    def post(self, request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        _client = ClientCreator.from_callibri_request(request)
    
        return JsonResponse({"status": "OK"}, status=200)