from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.product import Product
from store.models.category import Category
from store.models.brand import Brand
from django.views import View
from store.models.orders import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):

    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    brands = Brand.get_all_brand()
    brandID = request.GET.get('brand')
    results=request.GET.get("kw")
    k=request.GET.get('caution')
    customer = request.session.get('customer')
    if k:
        Order.objects.filter(id=k,customer=customer).delete()
        orders = Order.get_orders_by_customer(customer)
        messages.success(request, 'Order Item deleted Successfully')
        return render(request , 'orders.html'  , {'orders' : orders})
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    
        k=Category.objects.filter(id= categoryID)
    elif brandID:
        products = Product.get_all_products_by_brandid(brandID)
        k=brandID
    else:
        products = Product.get_all_products();
        k=None
    paginator=Paginator(products,6)
    page_number=request.GET.get('page')
    
    

    print(page_number)
    product_list = paginator.get_page(page_number)
        
    context={'product_list':product_list,'page_number':page_number,'k':k,'brands':brands,'categories':categories}


    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', context)
def search(request):
    if request.method=="POST":
        categories = Category.get_all_categories()
        brands = Brand.get_all_brand()
        searched=request.POST['searched']
        multiple_q=Q(Q(name__icontains=searched) | Q(description__icontains=searched))
        products=Product.objects.filter(multiple_q)
        paginator=Paginator(products,6)
        page_number=request.GET.get('page')
        print(page_number)
        product_list = paginator.get_page(page_number)
        context={'product_list':product_list,'searched':searched,'page_number':page_number,'brands':brands,'categories':categories}

        return render(request,'index.html', context)

        

def homepage(request):

    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    brands = Brand.get_all_brand()
    brandID = request.GET.get('brand')

    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    elif brandID:
        products = Product.get_all_products_by_brandid(brandID)

    else:
        products = Product.get_all_products();



    top_rated=Product.get_all_products_by_categoryid(1)
    featured=Product.get_all_products_by_categoryid(2)
    best_selling=Product.get_all_products_by_categoryid(3)
    electronics=Product.get_all_products_by_categoryid(4)
    shoes=Product.get_all_products_by_categoryid(5)
    computers=Product.get_all_products_by_categoryid(6)


    paginator1=Paginator(top_rated,2)
    paginator2=Paginator(featured,6)
    paginator3=Paginator(best_selling,6)
    paginator4=Paginator(electronics,6)
    paginator5=Paginator(shoes,6)
    paginator6=Paginator(computers,6)


    paginator=Paginator(products,6)
    page_number=request.GET.get('page')
    
    

    print(page_number)
    product_list = paginator.get_page(page_number)
    top_rated=paginator1.get_page(page_number)
    featured=paginator2.get_page(page_number)
    best_selling=paginator3.get_page(page_number)
    electronics=paginator4.get_page(page_number)
    shoes=paginator5.get_page(page_number)
    computers=paginator6.get_page(page_number)
        
    context={'product_list':product_list,'page_number':page_number,'brands':brands,'categories':categories ,'top_rated':top_rated,'featured':featured,'best_selling':best_selling,'electronics':electronics,'shoes':shoes,'computers':computers}


    print('you are : ', request.session.get('email'))
    return render(request, 'home.html', context)




def error_404_view(request, exception):
    return render(request,'404.html')