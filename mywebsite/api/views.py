import json
import os

from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from api.serializers import ProductSerializer

try:
    from dashboard.models import DashboardSetting
except:
    pass


class BaseAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    @classmethod
    def get_extra_actions(cls):
        return []

class DashboardSettingsView(BaseAPIView):
    def get(self, request):
        usersettings = {
                "1": [
                    {"id": 1, "title": "Night mode", "selected": False, "type": "lever"},
                    {"id": 2, "title": "Notifications", "selected": False, "type": "lever"},
                    {"id": 3, "title": "Réception d'emails", "selected": False, "type": "lever"}
                ]
            }
        return Response(data=usersettings)

    def post(self, request):
        # if request.data:
        #     user = DashboardSetting.objects.get(user='User')
        #     user.update(**request.data)
        #     if updated:
        #         return Response({'updated': True}, status=200)
        # return Response({'updated': False}, status=202)
        return Response({'updated': True}, status=200)

# class ProductsExample(ListAPIView):
#     """An API class to return a simple list of products"""
#     def list(self, request):
#         path = os.path.join(settings.MEDIA_ROOT, 'products.json')
#         with open(path, 'r', encoding='utf-8') as f:
#             data = json.load(f)['products']
#         serialized_data = ProductSerializer(data=data, many=True)
#         if serialized_data.is_valid():
#             return Response(data=serialized_data.data, status=200, content_type='application/json')
#         return Response(data={}, status=400, content_type='application/json')
    # @classmethod
    # def get_extra_actions(cls):
    #     return []


class ProductsExample(BaseAPIView):
    """An API class to return a simple list of products"""
    def get(self, request):
        path = os.path.join(settings.MEDIA_ROOT, 'products.json')
        with open(path, 'r', encoding='utf-8') as f:
            data =json.load(f)
        serialized_data = ProductSerializer(data=data['products'], many=True)
        if not serialized_data.is_valid():
            return Response(data=[], content_type='application/json')
        return Response(data=serialized_data.data)

class ProductExample(BaseAPIView):
    """Get a single product"""
    def get(self, request, **kwargs):
        path = os.path.join(settings.MEDIA_ROOT, 'products.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        item = [item for item in data['products'] if item['id'] == int(kwargs['pk'])]
        return Response(data=item, content_type='application/json')

class CreateProductExample(BaseAPIView):
    """Create a product example"""
    def post(self, request, **kwargs):
        try:
            for_update = request.data["update"]
            product_id = request.data["product_id"]
        except:
            product_id = None
            
        # try:
        #     path = os.path.join(settings.MEDIA_ROOT, 'products.json')
        #     with open(path, 'w+', encoding='utf-8') as f:
        #         data = json.load(f)
        #         last_id = int(data['products'][-1]['id'])
        #         request.data.update({'id': last_id + 1})
        #         data['products'].append(request.data)
        #         new_data = {
        #             'products': data
        #         }
        #         json.dump(new_data, f, indent=4)
        #     serialized_data = ProductSerializer(data=data['products'], many=True)
        # except:
        #     return Response(data=[], status=400)
        # else:
        #     if not serialized_data.is_valid():
        #         return Response(data={})
        #     return Response(data=serialized_data.data)
        return Response(data={'status': 'Product created', 'product_id': 1})

class DeleteProductExample(BaseAPIView):
    """Delete a product example"""
    def post(self, request, **kwargs):
        try:
            are_multiple = request.data["multiple"]
        except:
            are_multiple = False
        if are_multiple:
            # Delete multiple products here
            # by using a list of iDs
            return Response(data={'status': 'Products deleted', 'product_ids': [1, 2]})
        else:
            # Delete a single product
            return Response(data={'status': 'Product deleted', 'product_id': 1})

class RateUserView(BaseAPIView):
    """Rate a given user"""
    def post(self, request, **kwargs):
        return Response(data={'user': 'User was rated or created'})

class UserActionsView(BaseAPIView):
    """Do specific actions on a user such accept, refuse
    or stand by"""
    def post(self, request, **kwargs):
        actions = ['accept', 'refuse', 'meeting', 'standby']
        try:    
            requested_action = request.data['action']
        except KeyError:
            return Response(status=404)
        else:
            if requested_action not in actions:
                return Response(status=404)

            if requested_action == 'accept':
                pass
            elif requested_action == 'refuse':
                pass
            elif requested_action == 'meeting':
                pass
        return Response(data={'user': 'User was rated or created'})

class MessageUserView(BaseAPIView):
    """Message a given user"""
    def post(self, request, **kwargs):
        return Response(data={'message': 'User was messaged'})