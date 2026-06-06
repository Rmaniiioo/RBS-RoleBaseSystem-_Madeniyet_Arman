from django.shortcuts import render
from django.views import View
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework.views import APIView
from access_control.services import assert_can_access, can_access
from business.mock_data import MOCK_OBJECTS

 

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, "business/home.html")

class MockResourceView(APIView):
    permission_classes = [IsAuthenticated]
    element_code = None

    def get(self, request):
        assert_can_access(request.user, self.element_code, 'read')
        objects = MOCK_OBJECTS[self.element_code]
        visible = [
            item
            for item in objects
            if can_access(request.user, self.element_code, 'read', owner_id=item['owner_id'])
        ]
        return Response(visible)

    def post(self, request):
        assert_can_access(request.user, self.element_code, 'create')
        return Response(
            {
                "message": "Mock object created.",
                "element": self.element_code,
                "owner_id": request.user.id,
                "payload": request.data,
            },
            status=201
        )


class ProductView(MockResourceView):
    element_code = 'products'


class ShopView(MockResourceView):
    element_code = 'shops'


class OrderView(MockResourceView):
    element_code = 'orders'
