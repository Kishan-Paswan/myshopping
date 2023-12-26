from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator



# Create your models here.


class category(models.Model):
    category_name =models.CharField(max_length=50)
    category_image = models.ImageField(upload_to= 'media/category')

    def __str__(self):
        return self.category_name
 
class product(models.Model):
    product_name= models.CharField(max_length=50)
    product_title=models.CharField(max_length=50)
    product_image=models.ImageField(upload_to='media/product')
    product_price=models.IntegerField()
    product_category=models.ForeignKey(category,on_delete=models.CASCADE)

    

    def __str__(self):
        return self.product_name
    
class CartData(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    productId=models.ForeignKey(product,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    # productname= models.CharField(max_length=100, default="")
    # productprice= models.CharField(max_length=20, default="")
    # productimage= models.CharField(max_length=255, default="")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.productId.product_name
     

class billing(models.Model):
    user=models.ForeignKey  (User,on_delete=models.CASCADE)
    CartData=models.CharField(max_length=200)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    house_number=models.IntegerField()
    area=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    pincode=models.IntegerField()
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    paymentMode=models.CharField(max_length=20)
    paymentStatus=models.BooleanField(default=False)
    orederDate=models.DateField(auto_now_add=True,null=True,editable=True)
    

    def __str__(self):
        return self.first_name


class deliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")])
    house_number = models.CharField(max_length=20)
    area = models.CharField(max_length=50)
    landmark= models.CharField(max_length=50)
    pincode=models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country= models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(deliveryAddress, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.ManyToManyField(product) 
    paymentMode=models.CharField(max_length=20)
    paymentStatus=models.BooleanField(default=False)
    orederDate=models.DateField(auto_now_add=True,null=True,editable=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
class trackorder(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    orderId=models.ForeignKey(billing, on_delete=models.CASCADE)
    orderStatus=models.TextField()
    orderStatusDate = models.DateTimeField(auto_now_add=True)