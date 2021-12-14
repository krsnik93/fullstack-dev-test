import json

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views import View

from .models import Seller

class SellerById(View):
    def get(self, request, seller_id):
        try:
            seller = Seller.objects.get(id=seller_id)
            handle = seller.sellerhandle_set.get(active=True)

            return JsonResponse({
                'id': seller.id,
                'name': seller.name,
                'handle': handle.name
            })
        except ObjectDoesNotExist:
            return JsonResponse(status=404, data={ 'error': 'seller not found' })

    def put(self, request, seller_id):
        try:
            seller = Seller.objects.get(id=seller_id)
        except ObjectDoesNotExist:
            return JsonResponse(status=404, data={ 'error': 'seller not found'})

        params = json.loads(request.body)

        seller.name = params.get('name') or seller.name
        seller.save()

        new_handle = params.get('handle')
        active_handle = seller.sellerhandle_set.get(active=True)

        if new_handle and new_handle != active_handle.name:
            seller.sellerhandle_set.update(active=False)
            active_handle, created = seller.sellerhandle_set.get_or_create(
                name=new_handle, active=True
            )

        return JsonResponse({
            'id': seller.id,
            'name': seller.name,
            'handle': active_handle.name
        })


class SellerByHandle(View):
    def get(self, request, seller_handle):
        try:
            seller = Seller.objects.get(sellerhandle__name=seller_handle)

            return JsonResponse({
                'id': seller.id,
                'name': seller.name,
                'handle': seller_handle
            })
        except ObjectDoesNotExist:
            return JsonResponse(status=404, data={ 'error': 'seller not found' })
