"""
URL configuration for elaboratoecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from products.views import ProductViewSet, CategoryViewSet
from orders.views import CartView, CheckoutView, OrderListView, OrderStatusUpdateView

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/', include(router.urls)),
    path('api/cart/', CartView.as_view()),
    path('api/checkout/', CheckoutView.as_view()),
    path('api/orders/', OrderListView.as_view()),
    path('api/orders/<int:pk>/status/', OrderStatusUpdateView.as_view()),
]
