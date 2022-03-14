# Create your views here.
from braces.views import JSONRequestResponseMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View

from thesis.models import Order, Client
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
        # TODO: test with all utm labels
        client = ClientCreator.from_order_request(request)

        _order = Order.objects.create(client=client)

        return render(
            request,
            "index.html",
            {**PHONE_NUMBER_CONTEXT, "message": "Order is recorded"},
        )


class CallibriView(BaseOrderView):
    def post(self, request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        params = {k: v for k, v in request.POST.items()}

        _client = ClientCreator.from_callibri_request(request)

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
