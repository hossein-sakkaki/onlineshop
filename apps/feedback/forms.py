from django import forms

class CommentForm(forms.Form):
    product_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_text = forms.CharField(label='',
                                   error_messages={'requierd':'Field is requierd'},
                                   widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment text','rows':'4'}))