from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import category,product, CartData, billing,deliveryAddress,Order
from .forms import CartForm,checkoutForm,addressForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout




# Create your views here.

def home(request):
      return render(request,'shopapp/home.html')

def category_page(request):
       data=category.objects.all()
       context ={'data':data}
       return render(request,'shopapp/category.html',context,)

def product_page(request):
        data=product.objects.all()
        context={'data':data}
        return render(request,'shopapp/product.html',context)

def productbycategory(request, id):
      data=product.objects.filter(product_category=id)
      context={'data': data}
      return render(request,'shopapp/product.html',context)


def productdetails(request,id):
       data=product.objects.get(id=id)

       catid = data.product_category
       related = product.objects.filter(product_category=catid)

       context={'data': data, 'related': related}
       return render(request, 'shopapp/details.html',context)


@login_required
def account(request,id):
       return render( request, 'shopapp/account.html')


def signup(request):
       form = UserCreationForm()
       context ={'form': form}

       if request.method=='POST':
              form = UserCreationForm(request.POST)
              if form.is_valid():
                     form.save()
                     return redirect('login')
       return render(request, 'shopapp/signup.html',context) 


def login(request):
       form= AuthenticationForm
       if request.method=='POST':
              form = AuthenticationForm(request.POST,data=request.POST)
              if form.is_valid():
                     username=request.POST['username']
                     password=request.POST['password']
                     user=authenticate(username=username,password=password)

                     if User is not None:
                            auth.login(request,user)
                            return redirect('account', user.id)
                           
                     else:
                       return HttpResponse('incorrect username or password')

       return render(request, 'shopapp/login.html')


def logout_page(request):
       logout(request)
       return redirect('login')

@login_required
def cart(request):
       cart= CartData.objects.filter(user= request.user)
       cartTotal=0
       for x in cart:
             qty= x.qty
             price= x.productId.product_price
             cartTotal+= qty*price
       
       shipping=50
       total_amount=cartTotal+shipping   
                
             
             
       context= {'data': cart, 'total': cartTotal, 'totalAmount':total_amount,'shippingCharges':shipping}
       
       return render(request,'shopapp/cart.html', context)


# --------------------ADD TO CART ---------------------


@login_required
def add_to_cart(request):
              
       form= CartForm()
       if request.method=='POST':

              product = request.POST.get('productId')
              # cart= CartData.objects.filter(user= request.user, productId=product)
              # cart.qty +=1
              form=CartForm(request.POST)
              if form.is_valid():
                        existing_item = CartData.objects.filter(user= request.user,productId=product).first()

                        if existing_item:
                            existing_item.qty +=1
                            existing_item.save()
                        else:
                          form.save()
                          return redirect('cart')
              return redirect('product')



# -------------quantity update-----------------------
@login_required
def update_quantity(request):
      if request.method=='POST':
       cartid = request.POST.get('productId')
       operation = request.POST.get('operation')
       cart_item = CartData.objects.filter(user= request.user, id=cartid)

       if operation == 'increase':
             cart_item.qty +=1
       elif operation == 'decrease' and cart_item.qty > 1:
             cart_item.qty -= 1
       else:
             cart_item.delete()

       cart_item.save()      
       return redirect('cart')



# -------------delete product in cart---------------
@login_required
def deleteCartItem(request):
       if request.method=='POST':
           cartid = request.POST.get('productId')
           cart= CartData.objects.filter(user= request.user, id=cartid)
           cart.delete()
       return redirect('cart')

@login_required
def update(request):
        if request.method == 'POST':
             cart_id = request.POST.get('productId')
             new_qty_str = request.POST.get('qty')

             if new_qty_str:
                new_qty = int(new_qty_str)
            
                cart = CartData.objects.filter(user=request.user, id=cart_id).first()
            
                if cart:
                 cart.qty = new_qty
                 cart.save()

             return redirect('cart')
    
        return render(request, 'shopapp/cart.html')

#     if request.method == 'POST':
#         cart_id = request.POST.get('productId')
#         new_qty =  (request.POST.get('qty')) 

        
#         cart = CartData.objects.filter(user=request.user, id=cart_id).first()
        
#         cart.qty = new_qty
#         cart.save()
 
#         return redirect('cart')
#     return render(request, 'shopapp/cart.html')



@login_required
def checkout(request):
       cartid= CartData.objects.filter(user= request.user)

       totalAmount=0
       for x in cartid:
             qty=x.qty
             totalAmount +=x.productId.product_price*qty
   
     

       lst=[]
       for x in cartid:
              lst.append(x.productId.id)
       idstring = ', '.join(map(str, lst))
       
       context= {'cp': idstring, 'cartid':cartid, 'totalAmount': totalAmount}

       form = checkoutForm()
       if request.method == 'POST':
            form=checkoutForm(request.POST)
            if form.is_valid():
                  form.save()
                  return redirect('myorder')
              
       return render(request,'shopapp/checkout.html', context)


@login_required
def checkout_address(request):
     
       customer= billing.objects.get(user= request.user)
       context= { 'customer': customer}

       form = checkoutForm()
       if request.method == 'POST':
            form=checkoutForm(request.POST, instance=customer)
            if form.is_valid():
                  form.save()
                  return redirect('payment')

       return render(request,'shopapp/checkout.html', context)
                   
@login_required
def delivery_address(request):
       form = addressForm()
       context ={'form': form}

       if request.method=='POST':
              form = addressForm(request.POST)
              if form.is_valid():
                     form.save()
                     return redirect('place_order')
       return render (request,'shopapp/aadaddress.html',context)

@login_required
def place_order(request):
        cartid= CartData.objects.filter(user= request.user)

        totalAmount=0
        for x in cartid:
             qty=x.qty
             totalAmount +=x.productId.product_price*qty
   
        if request.method == 'POST':
            address_id = request.POST.get('addressId')
            print(address_id)
            changeAddress= deliveryAddress.objects.get(user=request.user,id=address_id)
           
        address=deliveryAddress.objects.filter(user=request.user)
        context={'address': address,'totalAmount': totalAmount}
        return render (request,'shopapp/placeorder.html',context)



@login_required
def payment(request):
      
      return render(request, 'shopapp/payment.html')

@login_required
def myorder(request):
     
      pl=[]
      cart= billing.objects.filter(user= request.user)
      for x in cart:
              productList= x.CartData.split(',')

      
      for x in productList:
              products= product.objects.get(id=x)
              pl.append(products)
       

      context={"myorder": cart, 'data': pl}
      return render(request, 'shopapp/myorder.html',context)


@login_required
def trackorder(request):
       return render(request, 'shopapp/trackorder.html')
