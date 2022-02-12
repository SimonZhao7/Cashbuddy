from django.forms import ModelForm, PasswordInput
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password1", "password2", "budget"]
        
    def clean(self):
        data = self.cleaned_data['username']
        if len(data) < 6:
            raise ValidationError("Usernaeme is too short")
        return super().clean()
        
        
class ChangeUsernameForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'password': PasswordInput()
        }
        
    def clean_username(self):
        value = self.cleaned_data['username']
        if len(value) < 6:
            raise ValidationError("Usernaeme is too short")
        return value
        
    def clean_password(self):
        value = self.cleaned_data['password']
        if not self.user.check_password(value):
            raise ValidationError('Incorrect Password')
        return value
        
    def save(self):
        self.user.username = self.cleaned_data['username']
        self.user.save()
        return self.user
    
    
class ChangeBudgetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = CustomUser
        fields = ['budget']
        
    def save(self):
        self.user.budget = self.cleaned_data['budget']
        self.user.save()
        return self.user
    
    
class ResetPasswordForm(SetPasswordForm):
    def clean(self):
        data = super().clean()
        if self.user.check_password(data['new_password1']):
            raise ValidationError('Your new passowrd can not be your current password')
        return data