from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    preferences = forms.CharField(label='Preferences', required=False)
    vm = forms.ChoiceField(choices=[('VM1','VM1'),('VM2','VM2')])

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    vm = forms.ChoiceField(choices=[('VM1','VM1'),('VM2','VM2')])
