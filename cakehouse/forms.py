from django import forms
from django.contrib.auth.forms  import UserCreationForm

from cakehouse.models import User,CakeCategory,Cake,CakeVarients,CakeOffers



# -----------------------Registration Form----------------------------------

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2','phone','address']
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password1":forms.PasswordInput(attrs={"class":"form-control"}),
            "password2":forms.PasswordInput(attrs={"class":"form-control"}),
            "phone":forms.TextInput(attrs={"class":"form-control"}),
            "address":forms.TextInput(attrs={"class":"form-control"})
        }

# --------------------Login Form---------------------------------------------

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


# -----------------------Category Add Form-------------------------------------

class CategoryAddForm(forms.ModelForm):
    class Meta:
        model=CakeCategory
        fields=['cat_name']

        widgets={
            "cat_name":forms.TextInput(attrs={"class":"form-control"})
        }

# -----------------------Cake Add Form-----------------------------------------

class CakeAddForm(forms.ModelForm):
    class Meta:
        model=Cake
        fields='__all__'
        
# -----------------------Cake Varient Add Form------------------------------------

class CakeVarientsAddForm(forms.ModelForm):
    class Meta:
        model=CakeVarients
        exclude=('cake',)

# ------------------------ Offer Add Form-----------------------------------------

class OfferAddForm(forms.ModelForm):
    class Meta:
        model=CakeOffers
        exclude=('cake_varient',)
        widgets={
            'start_date':forms.DateInput(attrs={'type':'date'}),
            'end_date':forms.DateInput(attrs={'type':'date'})
        }