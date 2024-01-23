from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView,TemplateView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator


from cakehouse.forms import RegistrationForm,LoginForm,CategoryAddForm,CakeAddForm,CakeVarientsAddForm,OfferAddForm
from cakehouse.models import User,CakeCategory,Cake,CakeVarients,CakeOffers

# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'invalid session')
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper   


def is_admin(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            messages.error(request,'permission denied for current user!!!')
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper


class SignUpView(CreateView):
    template_name='cakehouse/register.html'
    model=User
    form_class=RegistrationForm
    success_url=reverse_lazy('signin')

    def form_valid(self, form):
        messages.success(self.request,'Successfully created account')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to create account')
        return super().form_invalid(form)
    

# -----------------------------View for Login-------------------------------------------------------------

class SignInView(FormView):
    template_name='cakehouse/login.html'
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,'login successfully')
                return redirect('index')
            else:
                messages.error(request,'invalid username or password')
                return render(request,self.template_name,{'form':form})

desc=[signin_required,is_admin]

# --------------------------view for Category Adding and Listing------------------------------------------

@method_decorator(desc,name='dispatch')
class CakeCategoryAddView(CreateView,ListView):
    template_name='cakehouse/category_add.html'
    form_class=CategoryAddForm
    model=CakeCategory
    context_object_name='Categories'
    success_url=reverse_lazy('cat-add')

    def form_valid(self, form):
        messages.success(self.request,'Successfully Added Category')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Add Category')
        return super().form_invalid(form)
    
    def get_queryset(self):
        qs=CakeCategory.objects.filter(is_active=True)
        return qs


# -------------------------- View for Remove Category (inactive not delete)-------------------------------

@signin_required
@is_admin
def remove_categories(request,*args,**kwargs):
    id=kwargs.get('pk')
    CakeCategory.objects.filter(id=id).update(is_active=False)
    messages.success(request,'Category-removed')
    return redirect('cat-add')

# -------------------------- View for Add Cake------------------------------------------------------------

@method_decorator(desc,name='dispatch')
class CakeCreateView(CreateView):
    template_name='cakehouse/cake_add.html'
    form_class=CakeAddForm
    model=Cake
    success_url=reverse_lazy('cakes-list')

    def form_valid(self, form):
        messages.success(self.request,'Successfully Added Cake')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Add Cake')
        return super().form_invalid(form)
    

# --------------------View for List Cake------------------------------------------------------------

@method_decorator(desc,name='dispatch')
class CakeListView(ListView):
    template_name='cakehouse/cake_list.html'
    context_object_name='Cakes'
    model=Cake

# --------------------View for Update Cake------------------------------------------------------------

@method_decorator(desc,name='dispatch')
class CakeUpdateView(UpdateView):
    template_name='cakehouse/cake_edit.html'
    form_class=CakeAddForm
    model=Cake
    success_url=reverse_lazy('cakes-list')

    def form_valid(self, form):
        messages.success(self.request,'Successfully Updated Cake')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Update Cake')
        return super().form_invalid(form)
    
# ---------------------------View for Remove Cake-------------------------------------------------------

@signin_required
@is_admin
def remove_cake(request,*args,**kwargs):
    id=kwargs.get('pk')
    Cake.objects.filter(id=id).delete()
    messages.success(request,'Cake removed')
    return redirect('cakes-list')

# ---------------------------View for Add Cake Varients---------------------------------------------

@method_decorator(desc,name='dispatch')
class CakeVarientsAddView(CreateView):
    template_name='cakehouse/cake_varients_add.html'
    form_class=CakeVarientsAddForm
    model=CakeVarients
    success_url=reverse_lazy('cakes-list')

    def form_valid(self, form):
        id=self.kwargs.get('pk')
        obj=Cake.objects.get(id=id)
        form.instance.cake=obj
        messages.success(self.request,'Successfully Added Cake Varients')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Add Cake Varients')
        return super().form_invalid(form)

# ---------------------------View for Cake Details------------------------------------------------

@method_decorator(desc,name='dispatch')
class CakeDetailView(DetailView):
    template_name='cakehouse/cake_detail.html'
    model=Cake
    context_object_name='cake'

# ----------------------------View for Update Cake Varient -------------------------------------

@method_decorator(desc,name='dispatch')
class CakeVarientUpdateView(UpdateView):
    template_name='cakehouse/varient_edit.html'
    form_class=CakeVarientsAddForm
    model=CakeVarients
    success_url=reverse_lazy('cakes-list')

    def form_valid(self, form):
        messages.success(self.request,'Successfully Updated Cake Varients')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Update Cake Varients')
        return super().form_invalid(form)
    
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cake_varient_object=CakeVarients.objects.get(id=id)
        cake_id=cake_varient_object.cake.id
        return reverse("cake-detail",kwargs={"pk":cake_id})
    
# ----------------------------View for Remove Cake Varient----------------------------------------

@signin_required
@is_admin
def remove_cake_varient(request,*args,**kwargs):
    id=kwargs.get('pk')
    CakeVarients.objects.filter(id=id).delete()
    messages.success(request,'Cake Varient removed')
    return redirect('cakes-list')

# -------------------------View for Add Offers------------------------------------------------

@method_decorator(desc,name='dispatch')
class OffersAddView(CreateView):
    template_name='cakehouse/offers_add.html'
    form_class=OfferAddForm
    model=CakeOffers
    success_url=reverse_lazy('cakes-list')

    def form_valid(self, form):
        id=self.kwargs.get('pk')
        obj=CakeVarients.objects.get(id=id)
        form.instance.cake_varient=obj
        messages.success(self.request,'Successfully Added Offers')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Add Offers')
        return super().form_invalid(form)
    
    def get_success_url(self):
        # lh:8000/cakes/int:pk
        id=self.kwargs.get('pk')
        cake_varient_object=CakeVarients.objects.get(id=id)
        cake_id=cake_varient_object.cake.id
        return reverse('cake-detail',kwargs={'pk':cake_id})
        # return super().get_success_url()

# ------------------------- Remove Offer-----------------------------------------------

@signin_required
@is_admin
def remove_offers(request,*args,**kwargs):
    id=kwargs.get('pk')
    offer_object=CakeOffers.objects.get(id=id)
    cake_id=offer_object.cake_varient.cake.id
    offer_object.delete()
    messages.success(request,'Removed offer')
    return redirect('cake-detail',pk=cake_id)
 

@signin_required
@is_admin
def sign_out_view(request,*args,**kwargs):
    logout(request)
    return redirect('signin')


class IndexView(TemplateView):
    template_name='cakehouse/index.html'
