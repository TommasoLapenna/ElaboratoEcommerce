from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from products.models import Category, Product
from orders.models import Cart, CartItem, Order, OrderItem


User = get_user_model()

class Command(BaseCommand):
    help = "Scrpit per il seeding"


    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true',
                             help='Delete existing demo data before reseeding')

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            self._reset()

        self.stdout.write("Seeding users")
        users = self._seed_users()

        self.stdout.write("Seeding categories and products...")
        products = self._seed_catalog()

        self.stdout.write("Seeding cart")
        self._seed_cart(users['customer'], products)

        self.stdout.write("Seeding orders")
        self._seed_orders(users['customer'], products)

        self.stdout.write("Demo data seeded successfully.")

    def _reset(self):
        self.stdout.write("Resetting existing demo data")
        Order.objects.all().delete()
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(
            username__in=['admin_demo', 'manager_demo', 'user_demo', 'user2_demo']
        ).delete()

    def _seed_users(self):
        admin, _ = User.objects.get_or_create(username='admin_demo', defaults={
            'role': 'manager', 'is_staff': True, 'is_superuser': True,
            'email': 'admin@example.com'})
        admin.set_password('admin12345')
        admin.save()

        manager, _ = User.objects.get_or_create(username='manager_demo', defaults={
            'role': 'manager', 'email': 'manager@example.com'})
        manager.set_password('manager12345')
        manager.save()

        customer, _ = User.objects.get_or_create(username='user_demo', defaults={
            'role': 'customer', 'email': 'user@example.com'})
        customer.set_password('user12345')
        customer.save()

        customer2, _ = User.objects.get_or_create(username='user2_demo', defaults={
            'role': 'customer', 'email': 'user2@example.com'})
        customer2.set_password('user12345')
        customer2.save()

        return {'admin': admin, 'manager': manager, 'customer': customer, 'customer2': customer2}

    def _seed_catalog(self):
        catalog = {
            'Electronics': [
                ('Wireless Mouse', 19.99, 50),
                ('Mechanical Keyboard', 79.99, 20),
                ('USB-C Hub', 34.50, 0),
                ('Noise Cancelling Headphones', 129.99, 15),
            ],
            'Books': [
                ('Django for APIs', 29.99, 30),
                ('Clean Code', 34.99, 25),
                ('The Pragmatic Programmer', 39.99, 10),
            ],
            'Clothing': [
                ('Cotton T-Shirt', 14.99, 100),
                ('Denim Jacket', 59.99, 12),
                ('Running Shoes', 89.99, 8),
            ],
            'Home and Kitchen': [
                ('French Press', 24.99, 40),
                ('Cast Iron Skillet', 44.99, 18),
            ],
            'Sports': [
                ('Yoga Mat', 22.00, 60),
                ('Adjustable Dumbbell Set', 149.99, 5),
            ],
        }

        products = {}
        for cat_name, items in catalog.items():
            slug = cat_name.lower().replace(' & ', '-').replace(' ', '-')
            category, _ = Category.objects.get_or_create(name=cat_name, slug=slug)
            for name, price, stock in items:
                p_slug = name.lower().replace(' ', '-').replace("'", '')
                product, _ = Product.objects.get_or_create(
                    slug=p_slug,
                    defaults={'name': name, 'category': category, 'price': price,
                              'stock': stock, 'description': f'A great {name.lower()}.'}
                )
                products[p_slug] = product
        return products

    def _seed_cart(self, customer, products):
        cart, _ = Cart.objects.get_or_create(user=customer)
        for slug in ['wireless-mouse', 'django-for-apis']:
            product = products.get(slug)
            if product:
                CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})

    def _seed_orders(self, customer, products):
        if Order.objects.filter(user=customer).exists():
            return  # already seeded, don't duplicate on repeated runs

        order_specs = [
            ('paid', [('mechanical-keyboard', 1), ('cotton-t-shirt', 2)]),
            ('shipped', [('yoga-mat', 1)]),
            ('pending', [('clean-code', 1), ('french-press', 1)]),
        ]
        for status, items in order_specs:
            order = Order.objects.create(user=customer, status=status, total_price=0)
            total = 0
            for slug, qty in items:
                product = products.get(slug)
                if not product:
                    continue
                OrderItem.objects.create(order=order, product=product, quantity=qty, price=product.price)
                total += product.price * qty
            order.total = total
            order.save()