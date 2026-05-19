from django.db import models

# Create your models here.

class Genders(models.Model):
    class Meta:
        db_table = 'genders_tbl'
    gender_id = models.BigAutoField(primary_key=True, blank=False)
    gender = models.CharField(max_length=55, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Users(models.Model):
    class Meta:
        db_table = 'users_tbl'
    user_id = models.BigAutoField(primary_key=True, blank=False)
    full_name = models.CharField(max_length=64, blank=False)
    gender = models.ForeignKey(Genders, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=False)
    address = models.CharField(max_length=254, blank=False)
    contact_number = models.CharField(max_length=16, blank=True)
    email = models.CharField(max_length=128, blank=True)
    username = models.CharField(max_length=64, blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=False, unique=False, default='profile_pics/default_profile_pic.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Admin(models.Model):
    class Meta:
         db_table = 'admin_tbl'
    admin_id = models.BigAutoField(primary_key=True, blank=False)
    full_name = models.CharField(max_length=64, blank=False)
    address = models.CharField(max_length=254, blank=False)
    contact_number = models.CharField(max_length=16, blank=True)
    email = models.CharField(max_length=128, blank=True)
    username = models.CharField(max_length=64, blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Gender(models.Model):
    class Meta:
        db_table = 'product_gender_tbl'
    product_gender_id = models.BigAutoField(primary_key=True, blank=True)
    product_gender = models.CharField(max_length=128, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Products(models.Model):
    class Meta:
        db_table = 'product_tbl'
    product_id = models.BigAutoField(primary_key=True, blank=True)
    product_name = models.CharField(max_length=128, blank=False)
    product_brand = models.CharField(max_length=128, blank=False)
    product_image = models.ImageField(upload_to='product_img/', blank=False, unique=False)
    product_gender = models.ForeignKey(Product_Gender, on_delete=models.CASCADE)
    product_price = models.IntegerField(default=0, blank=False)
    product_quantity = models.IntegerField(default=0, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Payment(models.Model):
    class Meta:
        db_table = 'payment_tbl'
    payment_id =  models.BigAutoField(primary_key=True, blank=True)
    payment_method = models.CharField(max_length=128, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class History(models.Model):
    class Meta:
        db_table = 'history_tbl'
    history_id =  models.BigAutoField(primary_key=True, blank=True)
    buyer = models.ForeignKey(Users, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=False)
    payment_method = models.ForeignKey(Payment, on_delete=models.CASCADE)
    product_price = models.IntegerField(default=1, blank=False)
    # @property
    # def product_price(self):
    #     return self.product.product_price
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cart(models.Model):
    class Meta:
        db_table = 'cart_tbl'
    cart_id =  models.BigAutoField(primary_key=True, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_price = models.IntegerField(default=1, blank=False)
    quantity = models.IntegerField(default=0, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
