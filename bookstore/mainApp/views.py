from django.http import JsonResponse
from django.shortcuts import render
from .models import *

posts = [
    {
        'author':'CoreyMS',
        'title':'Blog Post',
        'content': '1st post content',
        'date_posted': 'August 27, 2018',
    },
    {
        'author':'Aruzhan',
        'title':'Blog Post 2',
        'content': '2st post content',
        'date_posted': 'August 28, 2018',
    }
]
def home(request):
    # context = {
    #     'posts': Post.objects.all()
    # }
    search = request.GET.get('searchh','')
    if search:
        posts = Post.objects.filter(title__icontains=search)
    else:
        posts = Post.objects.all();
    return render(request, 'mainApp/index.html',{'posts':posts})

def about(request):
    return render(request, 'mainApp/about.html',{'title' : 'About'})

# def register(request):
#     if request.method=='post':
#         email=request.post.get('email')
#         password=request.post.get('password')
#         user=User(email=email, password=password)
#         user.save()
#     return render(request,'mainApp/registration.html')

# def login(request):
#     return render(request,'mainApp/login.html')

def subpage(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request,'mainApp/subpage.html', {"post":post})

def cart(request):
    return render(request,'mainApp/cart.html')

def newReleases(request):
    post = Post.objects.order_by('-date_posted')[:5]
    return render(request,'mainApp/NewReleases.html', {"posts":post})

def cat_find(request, category_id):
    if category_id==0:
        posts = Post.objects.all()
    else:
        category = Category.objects.get(id=category_id)
        posts = Post.objects.filter(category=category)
    return render(request, 'mainApp/index.html', {'posts':posts})


def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories
    }
    return render(request, 'mainApp/cart.html', context)


def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    products = Post.objects.get(slug=product_slug)
    cart.add_to_cart(products.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()

    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Post.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.change_qty(qty, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse(
        {'cart_total': cart.items.count(),
         'item_total': cart_item.item_total,
         'cart_total_price': cart.cart_total})
