from django.shortcuts import render, redirect
from .models import CustomUser
from django.views import View
from .forms import UserRegisterForm, VerifyRegisterCodeForm
from django.contrib import messages
import utils

# Create your views here.
class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, 'accounts_app/register.html',{'form':form})
    
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
                'active_code': str(new_active_code)
            }
            
            messages.success(request,'Registration was successful','success')
            return redirect('main:index')
        
        messages(request,'Registration faild','danger')
        
class VerifyRegisterCodeView(View):
    def get(self, request, *args, **kwargs):
        form = VerifyRegisterCodeForm()
        return render(request, 'accounts_app/verify_code.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = VerifyRegisterCodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            if data['active_code'] == user_session['active_code']:
                user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                user.is_active=True
                user.active_code = utils.create_active_code(5)
                user.save()
                