from django.db import models

# Create your models here.

class User(models.Model):
    Name=models.CharField(max_length=40)
    Email=models.EmailField()
    Contact=models.IntegerField()
    Image=models.ImageField(upload_to='image')
    Pass=models.CharField(max_length=20)
    CPass = models.CharField(max_length=20, default='')


class Department(models.Model):
    dep_name=models.CharField(max_length=40)
    dep_desc=models.CharField(max_length=40)
    dep_head=models.CharField(max_length=40) 


class Add_Employee(models.Model):
    Name=models.CharField(max_length=40)
    Email=models.EmailField()
    Contact=models.IntegerField()
    Image=models.ImageField(upload_to='image')
    Code=models.CharField(max_length=20)
    Dept=models.CharField(max_length=20)

class Query(models.Model):
    Name=models.CharField(max_length=40)
    Email=models.EmailField(max_length=40)
    Emp_id=models.CharField(max_length=40)
    Dept=models.CharField(max_length=40)
    Query=models.CharField(max_length=80)
    Status=models.CharField(default="pending")
    Reply=models.CharField(max_length=80,null=True)
    

class Item(models.Model):
    item_name=models.CharField(max_length=40)
    item_desc=models.CharField(max_length=40)
    item_price=models.IntegerField()
    item_image=models.ImageField(upload_to='image')
    item_color=models.CharField(max_length=20)
    item_category=models.CharField(max_length=40)
    item_quantity=models.IntegerField(null=True)

class Order(models.Model):
    order_id=models.CharField(max_length=100 )
    amount=models.IntegerField()
    razorpay_id=models.CharField(max_length=100 ,blank=True)
    status=models.BooleanField(default=False )

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    