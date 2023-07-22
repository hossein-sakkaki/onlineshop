from django import forms
from .models import PaymentType

class OrderForm(forms.Form):
    name = forms.CharField(label='',
                           error_messages={'requierd':'This field should not be empty'},
                           widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}))
    
    family = forms.CharField(label='', 
                            error_messages={'requierd':'This field should not be empty'}, 
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Family'}))
    
    email = forms.EmailField(label='', 
                            error_messages={'requierd':'This field should not be empty'}, 
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Email'}),
                            required=False)
    
    phone_number = forms.CharField(label='', 
                            error_messages={'requierd':'This field should not be empty'},
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Phone Number'}),
                            required=False)
    
    address = forms.CharField(label='',
                            error_messages={'requierd':'This field should not be empty'},
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address','rows':'2'}))
    
    description = forms.CharField(label='',
                            error_messages={'requierd':'This field should not be empty'},
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description','rows':'4'}),
                            required=False)
    
    # payment_type = forms.ChoiceField(label='',
    #                         choices=[(item.pk, item)for item in PaymentType.objects.all()],
    #                         widget=forms.RadioSelect())