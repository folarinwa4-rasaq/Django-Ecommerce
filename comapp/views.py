from django.shortcuts import render,redirect
from.models import customer,Product,Cart,OrderPlaced,Payment,Wishlist
from django.views import View
from .forms import CustomerRegisterionForm,CustomerProfileForm,SearchForm
from django.contrib import messages,auth
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

@login_required
def home(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'comapp/home.html',{'totalitem':totalitem})

@login_required
def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'comapp/about.html',{'totalitem':totalitem})

@login_required
def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'comapp/contact.html',{'totalitem':totalitem})

@login_required
def category(request,val):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    prod = Product.objects.filter(category=val)
    title = Product.objects.filter(category=val).values('title')
    return render(request,'comapp/category.html',{'product':prod,'title':title,'totalitem':totalitem})

@login_required
def ProductDetail(request,pk):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    prod = Product.objects.get(pk=pk)
    wishlist = Wishlist.objects.filter(Q(product=prod) & Q(user=request.user))
    return render(request,'comapp/productdetail.html',{'product':prod,'totalitem':totalitem})

def CustomerRegisterion(request):
    form = CustomerRegisterionForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request,'Congratulations! Registation Successful')
    else:
        messages.warning(request, 'Invalid Data')
    return render(request,'comapp/customer-registeration.html',{'form':form})

@login_required
def Profile(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
        user = request.user
        name = form.cleaned_data['name']
        locality = form.cleaned_data['locality']
        city = form.cleaned_data['city']
        mobile = form.cleaned_data['mobile']
        state = form.cleaned_data['state']
        zipcode = form.cleaned_data['zipcode']

        reg = customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
        reg.save()
        messages.success(request,'Congratulations! Profile Save Successful')
    else:
        messages.warning(request,'Invalid Data Input')
    return render(request,'comapp/profile.html',{'form':form,'totalitem':totalitem})

@login_required
def Address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = customer.objects.filter(user=request.user)
    return render(request, 'comapp/address.html',{'add':add,'totalitem':totalitem})

@method_decorator(login_required,name='dispatch')
class UpdateAddressView(View):
    def get(self,request,pk):
        #add = customer.objects.get(pk=pk)
        form = CustomerProfileForm()
        return render(request,'comapp/UpdateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = customer.objects.get(pk=pk)                                                            
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,'Congratulations! Profile Update Successful')
        else:
            messages.warning(request,'Invalid Data Input')
        return redirect('address')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def add_to_cart(request,product_id):
    user=request.user
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/show-cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request,'comapp/add_to_cart.html',{'cart':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})

@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user=request.user
    add=customer.objects.filter(user=user)
    cart_item=Cart.objects.filter(user=user)
    famount = 0
    for p in cart_item:
        value = p.quantity *p.product.discounted_price
        famount =famount + 40
    totalamount = famount + 40

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount':20.00,
        'item_name':Product.title,
        'invoice':str(uuid.uuid4()),
        'currency_code':'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paymentdone')}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}"
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'paypal': paypal_payment
    }

    return render(request, 'comapp/checkout.html', context)

@login_required
def payment_done(request):
    return render(request, 'payment-success.html')

@login_required
def payment_failed(request):
    return render(request, 'payment-failed.html')

@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'comapp/orders.html',{'order_placed':order_placed, 'totalitem':totalitem})

def plus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        amount = 0
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)    
    
def minus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)    
    
def remove_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required
def search(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    query = request.GET.get('query','')
    product = Product.objects.filter(Q(title=query))
    return render(request,'comapp/search.html', {'product':product, 'totalitem':totalitem})

def plus_wishlist(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'wishlist Added Successfully'
        }
        return JsonResponse(data) 

def minus_wishlist(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'wishlist Added Successfully'
        }
        return JsonResponse(data)