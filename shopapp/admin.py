from django.contrib import admin
from .models import category,product,CartData,billing,Order,deliveryAddress

# Register your models here.
admin.site.register(category)
admin.site.register(product)
admin.site.register(CartData)
admin.site.register(billing)


admin.site.register(deliveryAddress)
admin.site.register(Order)