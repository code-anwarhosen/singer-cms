from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter username', 'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter email', 'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter password', 'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password', 'class': 'form-control'
        })

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter username', 'class': 'form-control'})
    )
    password = forms.CharField(max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'class': 'form-control'})
    )

    def clean(self):
        super().clean()
        
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise forms.ValidationError("Invalid username or password")
            
            self.user = user
        return self.cleaned_data

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'first_name', 'last_name', 'email', 'bio']
    
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'bio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself...',
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control auth-file-input'
            })
        }
