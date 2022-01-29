from django.contrib import admin
from django.urls import path
from .views.home import Index , store,search,homepage
from .views.signup import signup
from .views.login import Login , Logout
from .views.viewproduct import details,checkout1,remove_to_cart,lart
from .views.checkout import checkout
from .views.orders import orders,delete
from .middlewares.auth import  auth_middleware
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store/', store , name='store'),
    path('homepage/', homepage , name='home'),
    path('remove_to_cart', remove_to_cart , name='remove_to_cart'),
    path('search/', search, name='search'),
    path('signup', signup, name='signup'),
    path('checkout1/', checkout1, name='checkout1'),
    path('accounts/login/',Login, name='login'),
    path('login',Login, name='login'),
    path('logout/', Logout , name='logout'),
    path('<int:id>/details/', details , name='details'),
    path('lart',auth_middleware(lart), name='lart'),
    path('check-out', checkout , name='checkout'),
    path('orders/', orders, name='orders'),
    path('<int:id>/delete/', delete , name='delete'),
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]
