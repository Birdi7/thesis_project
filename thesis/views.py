# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View

from thesis.models import Order
from thesis.utils.client_creator import ClientCreator


class IndexView(TemplateView):
    template_name = "index.html"


class CreateOrderView(View):
    def post(self, request):
        # TODO: test with all utm labels
        client = ClientCreator.from_request(request)
        
        _order = Order.objects.create(
            client=client
        )
        
        return HttpResponse(status=200)
        