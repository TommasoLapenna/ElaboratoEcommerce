from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product, Category
from orders.models import Order, OrderItem

User = get_user_model()

class Command(BaseCommand):
    help = "Seed demo data for grading"

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username='admin_demo', defaults={
            'role': 'manager', 'is_staff': True, 'is_superuser': True})
        admin.set_password('admin12345')
        admin.save()

        manager, _ = User.objects.get_or_create(username='manager_demo', defaults={'role': 'manager'})
        manager.set_password('manager12345')
        manager.save()

        customer, _ = User.objects.get_or_create(username='user_demo', defaults={'role': 'customer'})
        customer.set_password('user12345')
        customer.save()

        cat, _ = Category.objects.get_or_create(name='Electronics', slug='electronics')
        p1, _ = Product.objects.get_or_create(name='Wireless Mouse', slug='wireless-mouse',
            defaults={'category': cat, 'price': 19.99, 'stock': 50})
        p2, _ = Product.objects.get_or_create(name='Mechanical Keyboard', slug='mechanical-keyboard',
            defaults={'category': cat, 'price': 79.99, 'stock': 20})

        order = Order.objects.create(user=customer, total_price=19.99, status='paid')
        OrderItem.objects.create(order=order, product=p1, quantity=1, price=19.99)

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))