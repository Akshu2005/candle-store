from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Category, Product, Review, Wishlist, Order, OrderItem
from .cart import Cart

def home(request):
    q = request.GET.get('q', '')
    cat = request.GET.get('category', '')
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True).order_by('-created_at')

    if q:
        products = products.filter(name__icontains=q) | products.filter(description__icontains=q)
    if cat:
        products = products.filter(category__slug=cat)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/home.html', {
        'categories': categories,
        'products': page_obj,
        'query': q,
        'selected_cat': cat
    })

def category_products(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    products = cat.products.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/category.html', {'category': cat, 'products': page_obj})

def product_detail(request, slug):
    p = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': p})

@require_POST
def add_to_cart(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.add(p, qty)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    items, total = cart.items()
    return render(request, 'shop/cart_detail.html', {'items': items, 'total': total})

@require_POST
def cart_update(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    if qty <= 0:
        cart.remove(p)
    else:
        cart.add(p, qty, update_quantity=True)
    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(p)
    return redirect('cart_detail')

@login_required
def toggle_wishlist(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    wl, created = Wishlist.objects.get_or_create(user=request.user)
    if p in wl.products.all():
        wl.products.remove(p)
    else:
        wl.products.add(p)
    return redirect('product_detail', slug=p.slug)

@login_required
def wishlist_page(request):
    wl, _ = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'shop/wishlist.html', {'wishlist': wl})

@login_required
@require_POST
def post_review(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    rating = int(request.POST.get('rating', 5))
    comment = request.POST.get('comment', '')
    Review.objects.create(product=p, user=request.user, rating=rating, comment=comment)
    return redirect('product_detail', slug=p.slug)

@login_required
def checkout(request):
    cart = Cart(request)
    items, total = cart.items()
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total=total, paid=True)
        for it in items:
            OrderItem.objects.create(order=order, product=it['product'], quantity=it['quantity'], price=it['price'])
        cart.clear()
        return render(request, 'shop/checkout_success.html', {'order': order})
    return render(request, 'shop/checkout.html', {'items': items, 'total': total})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def order_history(request):
    orders = request.user.orders.order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})
