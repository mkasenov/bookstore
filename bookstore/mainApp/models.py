from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    type=models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    slug = models.SlugField(null=True)
    price = models.DecimalField(decimal_places=1,max_digits=100)
    def __str__(self):
        return self.title

class User(models.Model):
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class CartItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __unicode__(self):
        return "Cart item for product {0}".format(self.post.title)

class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __unicode__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        cart = self
        post = Post.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(post=post, item_total=post.price)
        cart_items = [item.post for item in cart.items.all()]
        if new_item.post not in cart_items:
                cart.items.add(new_item)
                cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        post = Post.objects.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.post == post:
                    cart.items.remove(cart_item)
                    cart.save()

    def change_qty(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()


