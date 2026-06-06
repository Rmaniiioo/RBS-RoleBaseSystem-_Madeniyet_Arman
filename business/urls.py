from django.urls import path
from .views import HomeView, ProductView, ShopView, OrderView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductView.as_view(), name="products"),
    path("shops/", ShopView.as_view(), name="shops"),
    path("orders/", OrderView.as_view(), name="orders"),
]