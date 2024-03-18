from django import forms
from django.contrib.auth.models import User
from .models import Profile


error = {
    'max_length': 'تعداد حروف کافی نمی باشد',
    'required':'این فیلد اجباری می باشد',
    'invalid': 'عبارت وارد شده فاقد ارزش می باشد',
}

class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=30, error_messages=error, widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))
    email_address = forms.EmailField(max_length=50, error_messages=error, widget=forms.EmailInput(attrs={'placeholder': 'آدرس ایمیل'}))
    first_name = forms.CharField(max_length=30, error_messages=error, widget=forms.TextInput(attrs={'placeholder': 'نام'}))
    last_name = forms.CharField(max_length=30, error_messages=error, widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}))
    password1 = forms.CharField(max_length=30, error_messages=error, widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}))
    password2 = forms.CharField(max_length=30, error_messages=error, widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز عبور'}))

    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('user exist')
        else:
            return User
    def clean_email_address(self):
        email = self.cleaned_data['email_address']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('.این ایمیل قبلا وارد شده است')
        else:
            return email
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('password not match')
        elif len(password2) < 8:
            raise forms.ValidationError('password must be more than 8 digits ')
        elif not any(x.isupper() for x in password2):
            raise forms.ValidationError('رمز باید شامل حداقل یک حرف بزرگ باشد')
        else:
            return password1

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']

class PhoneForms(forms.Form):
    phone = forms.IntegerField()

class CodeForm(forms.Form):
    code = forms.IntegerField()