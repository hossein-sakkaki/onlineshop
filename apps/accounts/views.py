from django.shortcuts import render, redirect
from .models import CustomUser, Customer
from .forms import UpdateProfileForm
from django.views import View
from .forms import UserRegisterForm, VerifyRegisterCodeForm, LoginUserForm, ChangePasswordForm, RememberPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from apps.payments.models import Payment


import utils

# Create your views here.
class UserRegisterView(View):
    template_name = 'accounts_app/register.html'
    
    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_active_code = utils.create_active_code(5)
            CustomUser.objects.create_user(
                mobile_number = data['mobile_number'],
                active_code = new_active_code,
                password = data["password1"],
            )
            utils.send_email(data['mobile_number'], f'Your activate code is: {new_active_code}')
            request.session['user_session'] = {
                'mobile_number': data['mobile_number'],
                'active_code': str(new_active_code),
                'remember_password': False,
            }
            
            messages.success(request,'Registration is in progress, Please enter the code.','success')
            return redirect('accounts:verify')
        
        messages(request,'Registration faild','danger')
        
class VerifyRegisterCodeView(View):
    template_name = 'accounts_app/verifycode.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = VerifyRegisterCodeForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = VerifyRegisterCodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            if data['active_code'] == user_session['active_code']:
                user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                if user_session['remember_password'] == False:
                    user.is_active=True
                    user.active_code = utils.create_active_code(5)
                    user.save()
                    messages.success(request,'Registration was successful','success')
                    return redirect('main:index')
                else:
                    return redirect('accounts:change_password')
            else:
                messages.error(request, 'Code is wrong', 'danger')
                return render(request, self.template_name, {'form': form})
            
        messages.error(request,'The informatin is not valid','danger')
        return render(request, self.template_name, {'form': form})
    
    
class LoginUserView(View):
    template_name = 'accounts_app/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request, *args, **kwargs):
        form = LoginUserForm()
        return render(request, self.template_name ,{'form': form})
                
    def post(self,request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['mobile_number'], password=data['password'])
            if user is not None:
                db_user = CustomUser.objects.get(mobile_number=data['mobile_number'])
                if db_user.is_admin == False:
                    messages.success(request, 'Welcome Back!', 'success')
                    login(request, user)                        
                    next_url = request.GET.get('next')
                    if next_url is not None:
                        return redirect(next_url)
                    else:
                        return redirect('main:index')
                else:
                    messages.error(request, 'You are is Admin. You must login admin page. Good Luck!', 'warning')
                    return render(request, self.template_name, {'form': form})
            else:    
                messages.error(request, 'The information is incorrect', 'danger')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'The information is invalid', 'danger')
            return render(request, self.template_name, {'form': form})
                
class LogoutUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        session_data = request.session.get('shop_cart')
        logout(request)
        request.session['shop_cart'] = session_data
        return redirect('main:index')
    
    
class ChangePasswordView(View):
    template_name = 'accounts_app/changepassword.html'
    
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            user.set_password(data['password1'])
            user.active_code = utils.create_active_code
            user.save()
            messages.success(request,'Your password has been changed','success')
            return redirect('accounts:login')
        else:
            messages.error(request,'Your information is NOT valid','danger')
            return render(request, self.template_name, {'form':form})
    
class RememberPasswordView(View):
    template_name = 'accounts_app/rememberpassword.html'
    
    def get(self, request, *args, **kwargs):
        form = RememberPasswordForm()
        return render(request, self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = RememberPasswordForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                user = CustomUser.objects.get(mobile_number = data['mobile_number'])
                if user.is_admin == False:
                    active_code = utils.create_active_code(5)
                    user.active_code = active_code
                    user.save()
                    
                    utils.send_sms(data['mobile_number'], f'Your copde is {active_code}')
                    request.session['user_session'] = {
                        'active_code': str(active_code),
                        'mobile_number': data['mobile_number'],
                        'remember_password': True,
                    }
                    messages.success(request,'Please submit your code','success')
                    return redirect('accounts:verify')
                else:
                    messages.error(request, 'You are is Admin. You can change password in admin page!', 'warning')
                    return render(request, self.template_name, {'form': form}) 
            except:
                messages.error(request,'Mobile number does not exist','danger')
                return render(request, self.template_name,{'form':form})


# class UserPanelView(LoginRequiredMixin, View):
#     template_name= 'accounts_app/userpanel.html'
    
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('main:index')
#         return super().dispatch(request, *args, **kwargs)
    
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

class UserPanelView(LoginRequiredMixin, View):
    template_name= 'accounts_app/userpanel.html'
    
    def get(self, request, *args, **kwargs):
        user = request.user 
        try:
            customer = Customer.objects.get(user = request.user)
            user_info = {
                'name': user.name,
                'family': user.family,
                'email': user.email,
                'mobile_number': customer.mobile_number,
                'adress': customer.address,
                'image': customer.image_name,
            }
        except ObjectDoesNotExist:
            user_info = {
                'name': user.name,
                'family': user.family,
                'email': user.email,
            }
        return render(request, self.template_name, {'user_info': user_info})
    
class UpdateProfileView(View):
    def get(self, request):
        user = request.user 
        try:
            customer = Customer.objects.get(user = request.user)
            initial_dict = {
                'mobile_number': user.mobile_number,
                'name': user.name,
                'family': user.family,
                'email': user.email,
                
                'phone_number': customer.phone_number,
                'adress': customer.address,
            }
        except ObjectDoesNotExist:
            initial_dict = {
                'mobile_number': user.mobile_number,
                'name': user.name,
                'family': user.family,
                'email': user.email,
            }
        form = UpdateProfileForm(initial = initial_dict)
        return render(request,'accounts_app/update_profile.html',{'form': form, 'image_url':customer.image_name})
    
    def post(self, request):
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            user.name = data['name']
            user.family = data['family']
            user.email = data['email']
            user.save()
            try:
                customer = Customer.objects.get(user = request.user)
                customer.phone_number = data['phone_number']
                customer.address = data['address']
                customer.image_name = data['image']
                customer.save()
            except ObjectDoesNotExist:
                Customer.objects.create(
                    user = request.user,
                    phone_number = data['phone_number'],
                    address = data['address'],
                    image = data['image'],
                )
            messages.success(request,'Your edit profile is done!','success')
            return redirect('accounts:userpanel')
        else:
            messages.error(request,'The entered information is Not Valid','danger')
            return render(request, 'accounts_app/update_profile.html',{'form': form})
     
@login_required       
def show_user_payments(request):
    payments = Payment.objects.filter(customer_id=request.user.id).order_by('-register_date') 
    return render(request, 'accounts_app/show_user_payments.html',{'payments': payments} )
 


@login_required
def show_last_orders(request):
    orders = Order.objects.filter(customer_id = request.user.id).order_by('-register_date')[:4]
    return render(request, 'accounts_app/partials/show_last_orders.html',{'orders': orders} )

@login_required
def show_user_payments(request):
    payments = Payment.objects.filter(customer_id = request.user.id).order_by('-register_date')
    return render(request, 'accounts_app/partials/show_user_payments.html',{'payments': payments} )