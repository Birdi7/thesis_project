# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View

from thesis.utils.client_creator import ClientCreator


class IndexView(TemplateView):
    template_name = "index.html"


class PurchaseView(View):
    def post(self, request):
        # TODO: test with all utm labels
        ClientCreator.from_request(request)
        
        return HttpResponse(status=200)
        