from django.shortcuts import render , redirect
from django.contrib.auth.hashers import  check_password
from django.views import  View
from store.models.product import  Product
from store.models.category import  Category
from store.models.brand import  Brand
from .forms import OrderForm,ViewCartForm
from django.contrib.auth.decorators import login_required
from store.middlewares.auth import auth_middleware


def lart(request):
    ids = list(request.session.get('cart').keys())
    products = Product.get_products_by_id(ids)
    print(products)
    return render(request , 'cart.html' , {'products' : products} )



def details(request, id):
    form=ViewCartForm()
    if request.method=='POST':
        product = request.POST.get('product')
        cart = request.session.get('cart')
        quantitey = cart.get(product)
        form=ViewCartForm(request.POST)
        if form.is_valid():
            cart[product] = form.cleaned_data.get('quantity')
    product=Product.objects.get(id=id)
    context={'product':product,'form':form}
    cart = request.session.get('cart')

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    



    return render(request , 'viewproduct.html',context)

@login_required(login_url='login')
def checkout1(request):
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    brands = Brand.get_all_brand()
    brandID = request.GET.get('brand')
    if request.method=='POST':
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        elif brandID:
            products = Product.get_all_products_by_brandid(brandID)
        paginator=Paginator(products,6)
        page_number=request.GET.get('page')
    
    

        print(page_number)
        product_list = paginator.get_page(page_number)
        return render(request , 'index.html',{'product_list' : product_list,'categories':categories,'brands':brands})
    return render(request , 'checkout1.html',{'categories':categories,'brands':brands})

def remove_to_cart(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('lart')




