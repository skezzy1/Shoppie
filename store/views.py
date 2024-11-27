from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm, SubscribeForm
from .models import Blog, Product, Cart, CartItem, Order, OrderItem
from .forms import BlogPostForm, ProductForm
from django.http import JsonResponse
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    formCon = ContactForm()
    formSub = SubscribeForm()
    return render(request, 'store/index/index.html', {'form': formCon, 'subscribe': formSub })

def aboutUs(request):
    formCon = ContactForm()
    formSub = SubscribeForm()
    return render(request, 'store/aboutUs/aboutUs.html', {'form': formCon, 'subscribe': formSub })

def shop(request):
    formCon = ContactForm()
    formSub = SubscribeForm()

    if request.method == 'POST':
        if 'contact_submit' in request.POST:  
            formCon = ContactForm(request.POST)
            if formCon.is_valid():
                formCon.save() 
        elif 'subscribe_submit' in request.POST:  
            formSub = SubscribeForm(request.POST)
            if formSub.is_valid():
                formSub.save()  
    return render(request, 'store/shope/shop.html', {
        'form': formCon, 
        'subscribe': formSub  
    })
def sync_cart(request):
    if request.user.is_authenticated:
        cart = request.COOKIES.get('cart', '{}')
        cart = json.loads(cart)

        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            CartItem.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': item['quantity']},
            )
        return JsonResponse({'message': 'Cart synchronized!'})
    return JsonResponse({'message': 'User not logged in!'})
#Forms
def send_contact_view(request):
    if request.method == 'POST':
        formCon = ContactForm(request.POST)
        if formCon.is_valid():
            formCon.save()
            return JsonResponse({'message': 'Thank you for contacting us!', 'status': 'success'})
        else:
            errors = formCon.errors.as_json()
            return JsonResponse({'message': errors, 'status': 'error'}, status=400)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)

def subscribe_newsletter(request):
    if request.method == 'POST':
        formSub = SubscribeForm(request.POST)
        if formSub.is_valid():
            formSub.save()
            return JsonResponse({'message': 'Thank you for subscribing!', 'status': 'success'})
        else:
            errors = formSub.errors.as_json()
            return JsonResponse({'message': errors, 'status': 'error'}, status=400)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)

#blog
def blog(request):
    formCon = ContactForm()
    formSub = SubscribeForm()
    posts = Blog.objects.all().order_by('-created_at')  
    return render(request, 'store/blog/blog.html', {'posts': posts, 'form': formCon, 'subscribe': formSub})

def blog_detail(request, post_id):
    post = get_object_or_404(Blog, id=post_id) 
    return render(request, 'store/blog/blog_detail.html', {'post': post})

def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogPostForm()
    return render(request, 'store/blog/create_blog_post.html', {'form': form})
def edit_blog_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)  
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)  
        if form.is_valid():
            form.save() 
            return redirect('blog_detail', post_id=post.id) 
    else:
        form = BlogPostForm(instance=post) 
    
    return render(request, 'store/blog/edit_blog_post.html', {'form': form, 'post': post})
def delete_blog_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)  
    if request.method == 'POST':
        post.delete() 
        return redirect('blog')  
    return render(request, 'store/blog/delete_blog_post.html', {'post': post}) 

#Cart
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/shop/shop_detail.html', {'product': product})

def cart(request):
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    for item in cart.values():
        item['total'] = item['price'] * item['quantity']

    return render(request, 'store/cart/cart.html', {
        'cart': cart.values(), 
        'total_price': total_price
    })

def cart(request):
    cart = request.session.get('cart', {})
    formatted_cart = format_cart_items(cart)
    total_price = sum(item['total_price'] for item in formatted_cart)

    return render(request, 'store/cart/cart.html', {
        'cart': formatted_cart,
        'total_price': total_price
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    for product_id, sizes in cart.items():
        product = Product.objects.get(id=product_id)
        for size, details in sizes.items():
            cart_items.append({
                'id': product_id,
                'name': product.title,
                'image_url': product.image.url,
                'price': product.price,
                'size': size,
                'quantity': details['quantity'],
                'total_price': product.price * details['quantity'],
            })

    total_price = sum(item['total_price'] for item in cart_items)

    context = {
        'cart': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]
    request.session['cart'] = cart
    return JsonResponse({'message': 'Quantity updated', 'cart_items': format_cart_items(cart)})

def delete_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart: 
        del cart[str(product_id)]
    request.session['cart'] = cart
    request.session.modified = True 
    return redirect('cart')

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1 
    else:
        cart[product_id] = 1  
    request.session['cart'] = cart
    request.session.modified = True 
    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1  
        else:
            del cart[product_id]  
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def format_cart_items(cart):
    items = []
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        items.append({
            'id': product.id,
            'name': product.title,
            'quantity': quantity,
            'price': product.price,
            'total_price': product.price * quantity,
            'image_url': product.image.url if product.image else ''
        })
    return items

def checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        total_price = request.POST.get('total_price')

        if not full_name or not address or not email or not phone:
            messages.error(request, "Please fill out all fields.")
            return redirect('checkout')

        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty!")
            return redirect('cart')

        total_price = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id) 
            total_price += product.price * quantity 

        user = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
            user=user,
            customer_name=full_name,
            address=address,
            email=email,
            phone=phone,
            total_price=total_price
        )

        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        request.session['cart'] = {}
        request.session.modified = True

        if user is None:
            messages.success(request, 'Ваше замовлення успішно оформлене!')

        return redirect('home')
    return render(request, 'store/cart/checkout.html')

@login_required 
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/cart/order_history.html', {'orders': orders})
@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'accounts/profile/profile.html', {'orders': orders})
#Shop
def shop(request):
    products = Product.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category=category_filter)
    price_range = request.GET.get('price_range')
    if price_range:
        low, high = map(int, price_range.split('-'))
        products = products.filter(price__gte=low, price__lte=high)
    return render(request, 'store/shop/shop.html', {'products': products})

def create_shop_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('shop')  
    else:
        form = ProductForm()
    return render(request, 'store/shop/сreate_product.html', {'form': form})

def edit_shop_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)  
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # Додано request.FILES
        if form.is_valid():
            form.save()
            return redirect('shop_detail', product_id=product.id)  
    else:
        form = ProductForm(instance=product)  
    return render(request, 'store/shop/edit_product.html', {'form': form, 'product': product})


def delete_shop_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)  
    if request.method == 'POST':
        product.delete() 
        return redirect('shop')  
    return render(request, 'store/shop/delete_product.html', {'product': product})
