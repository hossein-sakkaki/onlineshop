from django import forms

class CouponForms(forms.Form):
    coupon_code = forms.CharField(label='',
                                  error_messages={'requierd': 'This field can not empty'},
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Coupon code'}))