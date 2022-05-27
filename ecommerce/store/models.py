from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model): # customer model with one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) # one user has one customer, one customer has one user
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self): # for admin panel
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True, blank=True) # if it is digital - we don't need to ship it
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self): # return empty string if there are no image
        try:
            url = self.image.url
        except:
            url = ''
        return

class Order(models.Model): # it is our order-object
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) # many-to-one relationship, because customer can have multiple orders
    date_ordered = models.DateTimeField(auto_now_add=True) # change the value when the order is complete
    complete = models.BooleanField(default=False) # status of our cart
    transaction_id = models.CharField(max_length=100, null=True) # information for order

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model): # many-to-one relationship, because cart can have multiple order items
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address