from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Re-Password", widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['mobile_number','email','name','family','gender']
        
    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Your password is wrong or diffrente")
        return pass2
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='If you want change password <a href="../password">click here...</a>')
    
    class Meta:
        model = CustomUser
        fields = ['mobile_number','password','email','name','family','gender','is_active','is_admin']
        
#------------------------------------------------------------------------------------------------------
class UserRegisterForm(ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter the Password'}))
    password2 = forms.CharField(label="Re-Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter the Re-Password'}))
    
    class Meta:
        model = CustomUser
        fields = ['mobile_number']
        widgets = {
            'mobile_number': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Mobile Number'})
        }
        
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('Your password is wrong or diffrente')
        return pass2
    
class VerifyRegisterCodeForm(forms.Form):
    active_code = forms.CharField(label='Activate code',
                                  error_messages={'requierd':'This field is requierd'},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter the code'}))
    
class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(label='Phone Number',
                                  error_messages={'requierd':'This field is requierd'},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter Phone'}))
    
    password = forms.CharField(label='Password',
                                  error_messages={'requierd':'This field is requierd'},
                                  widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Please enter Password'}))
    
    
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='Password',
                                  error_messages={'requierd':'This field is requierd'},
                                  widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Please enter Password'}))
    password2 = forms.CharField(label='Password',
                                  error_messages={'requierd':'This field is requierd'},
                                  widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Please enter Re-Password'}))
    
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('Your password is wrong or diffrente')
        return pass2
    
class RememberPasswordForm(forms.Form):
    mobile_number = forms.CharField(label='Phone Number',
                                  error_messages={'requierd':'This field is requierd'},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter Phone'}))
    
    
class UpdateProfileForm(forms.Form):
    mobile_number = forms.TextInput(label='', error_messages={'This field should not be empty'}, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Mobile Number'}))
    name = forms.TextInput(label='', error_messages={'This field should not be empty'}, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Name'}))
    family = forms.TextInput(label='', error_messages={'This field should not be empty'}, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Family'}))
    email = forms.EmailInput(label='', error_messages={'This field should not be empty'}, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Email'}))
    phone_number = forms.TextInput(label='', error_messages={'This field should not be empty'}, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Phone Number'}))
    address = forms.Textarea(label='', error_messages={'This field should not be empty'}, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}))
    image = forms.ImageField(required=False)
    
    