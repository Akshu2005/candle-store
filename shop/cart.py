from decimal import Decimal
from .models import Product

class Cart:
    SESSION_KEY = 'cart'

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if not cart:
            cart = self.session[self.SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[pid]['quantity'] = quantity
        else:
            self.cart[pid]['quantity'] += quantity
        self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def items(self):
        ids = [int(i) for i in self.cart.keys()]
        products = Product.objects.filter(id__in=ids)
        items = []
        total = 0
        for p in products:
            qty = int(self.cart[str(p.id)]['quantity'])
            subtotal = p.price * qty
            items.append({'product': p, 'quantity': qty, 'subtotal': subtotal, 'price': p.price})
            total += subtotal
        return items, total

    def get_total_price(self):
        _, total = self.items()
        return total
