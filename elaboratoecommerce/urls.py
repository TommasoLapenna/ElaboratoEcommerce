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
from django.http import HttpResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from products.views import ProductViewSet, CategoryViewSet
from orders.views import CartView, CheckoutView, OrderListView, OrderStatusUpdateView

def api_welcome(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>E-commerce API</title>
        <style>
        </style>
    </head>
    <body>
        <h1>E-Commerce API</h1>
        <p>Il server è attualmente <strong>ONLINE</strong> e funzionante.</p>
        
        <div>
            <a href="/api/" class="btn">Esplora gli Endpoint API</a>
            <a href="/admin/" class="btn" style="background-color: green;">Pannello di Amministrazione</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

router = DefaultRouter()

# Registrazione dei viewset
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)

# Mappatura degli url agli endpoint corrispondenti
urlpatterns = [
    path('', api_welcome),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/', include(router.urls)),
    path('api/cart/', CartView.as_view()),
    path('api/checkout/', CheckoutView.as_view()),
    path('api/orders/', OrderListView.as_view()),
    path('api/orders/<int:pk>/status/', OrderStatusUpdateView.as_view()),
]
