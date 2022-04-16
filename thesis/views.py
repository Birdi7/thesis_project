# Create your views here.
from braces.views import JSONRequestResponseMixin
from django.contrib.gis.geos import Point
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from thesis.models import Address, Client, Order
from thesis.utils.address import AddressParser
from thesis.utils.client_creator import ClientCreator

PHONE_NUMBER_CONTEXT = {"phone_number": "+7 999 999-99-99"}


class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = PHONE_NUMBER_CONTEXT


class BaseOrderView(View):
    def get(self, request: WSGIRequest):
        return render(request, "index.html", PHONE_NUMBER_CONTEXT)


class CreateOrderView(BaseOrderView):
    def post(self, request: WSGIRequest):
        address = AddressParser.from_string(request.POST["address"])
        client = ClientCreator.from_order_request(request)
        if address:
            address_model = Address.objects.create(location=Point(address.x, address.y))
            Order.objects.create(client=client, address=address_model)
        else:
            Order.objects.create(client=client)

        return render(
            request,
            "index.html",
            {**PHONE_NUMBER_CONTEXT, "message": "Order is recorded"},
        )


class CallibriView(BaseOrderView):
    def post(self, request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        params = {k: v for k, v in request.POST.items()}  # noqa
        # TODO: use params somehow
        ClientCreator.from_callibri_request(request)

        return JsonResponse({"status": "OK"}, status=200)


class VoximplantCreateOrderView(JSONRequestResponseMixin, BaseOrderView):
    def post(self, request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        phone = self.request_json["phone"]

        if not Client.objects.filter(phone=phone).exists():
            # client not found
            return JsonResponse({"status": "NOT_FOUND"}, status=400)

        # let's assume client is created by callibri requset
        client = Client.objects.filter(phone=phone)
        Order.objects.create(
            client=client
            # some other information can be sent from voximplant to be
            # saved in the order instance
        )

        return JsonResponse({"status": "OK"}, status=200)
