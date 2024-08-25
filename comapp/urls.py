from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import UpdateAddressView
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MypasswordChangeForm,MySetPasswordForm,MyPasswordResetForm
from django.contrib import admin

urlpatterns = [
    path('',views.home,name='home'),
    path('category/<str:val>/',views.category,name='category'),
    path('product-detail/<int:pk>/',views.ProductDetail,name='product-detail'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('profile/',views.Profile,name='profile'),
    path('address/',views.Address,name='address'),
    path('<str:pk>/',UpdateAddressView.as_view(),name='updateaddress'),
    path('search/',views.search,name='search'),
    #cart section
    path('add-to-cart/<int:product_id>/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='show-cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('paymentfailed/',views.payment_failed,name='paymentfailed'),
    path('pluscart/',views.plus_cart,name='pluscart'),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('removecart/',views.remove_cart,name='removecart'),
    path('pluswishlist/',views.plus_wishlist,name='pluswishlistt'),
    path('minuswishlist/',views.minus_wishlist,name='minuswishlistt'),
    path('orders/',views.home,name='orders'),
    # Auth Urls
    path('registeration/',views.CustomerRegisterion,name='customerregisterion'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='comapp/login.html', authentication_form=LoginForm),name='login'),
    path('logout/',views.logout,name='logout'), 
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='comapp/changepassword.html', form_class=MypasswordChangeForm,success_url='/passwordchangedone'),name='changepassword'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='comapp/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='comapp/password_reset.html', form_class=MyPasswordResetForm),name="password_reset"),
    path('password-reset-done/',auth_view.PasswordResetDoneView.as_view(template_name='comapp/password_reset_done.html'),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='comapp/password_reset_confirm.html', form_class=MySetPasswordForm),name="password_reset_confirm"),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='comapp/password_reset_complete.html'),name="password_reset_complete"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Welcome to Folly`s Dashboard'
admin.site.site_title = 'Folly`s Dashboard'
admin.site.site_index_title = ' Welcome to Folly project'