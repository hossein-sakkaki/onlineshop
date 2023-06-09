from django.urls import path
from . import views

app_name= 'accounts'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(), name='register'),
    path('verify/',views.VerifyRegisterCodeView.as_view(), name='verify'),
    path('login/',views.LoginUserView.as_view(), name='login'),
    path('logout/',views.LogoutUserView.as_view(), name='logout'),
    
    path('userpanel/',views.UserPanelView.as_view(), name='userpanel'), 
    path('show_last_orders',views.show_last_orders, name='show_last_orders'), 
    path('show_user_payments',views.show_user_payments, name='show_user_payments'), 
    path('change_password/',views.ChangePasswordView.as_view(), name='change_password'), 
    path('remember_password/',views.RememberPasswordView.as_view(), name='remember_password'), 
]