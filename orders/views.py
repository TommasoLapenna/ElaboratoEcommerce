from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from .serializers import OrderSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = [{"product": i.product.name, "quantity": i.quantity, "price": str(i.product.price)}
                 for i in cart.items.select_related('product')]
        return Response({"items": items})

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        if product.stock < quantity:
            return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
        if not created:
            item.quantity += quantity
            item.save()
        return Response({"message": "Added to cart"}, status=status.HTTP_201_CREATED)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            total = 0
            order = Order.objects.create(user=request.user, total=0)
            for item in cart.items.select_related('product'):
                if item.product.stock < item.quantity:
                    order.delete()
                    return Response({"error": f"Not enough stock for {item.product.name}"},
                                     status=status.HTTP_400_BAD_REQUEST)
                OrderItem.objects.create(order=order, product=item.product,
                                          quantity=item.quantity, price=item.product.price)
                item.product.stock -= item.quantity
                item.product.save()
                total += item.product.price * item.quantity
            order.total_price = total
            order.save()
            cart.items.all().delete()

        return Response({"order_id": order.id, "total_price": str(order.total_price)}, status=status.HTTP_201_CREATED)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'manager':
            orders = Order.objects.all().prefetch_related('items__product')
        else:
            orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class OrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.role != 'manager':
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        order = Order.objects.filter(pk=pk).first()
        if not order:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save()
        return Response({"id": order.id, "status": order.status})