from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator

from datetime import date

# Create your models here.

#----------------------User Model for authentication---------------------

class User(AbstractUser):
    phone=models.CharField(max_length=200,unique=True)
    address=models.CharField(max_length=200)

# ----------------------Category Model----------------------------------

class CakeCategory(models.Model):
    cat_name=models.CharField(max_length=200,unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.cat_name
    
# ----------------------Cake Model----------------------------------------

class Cake(models.Model):
    cat_name=models.ForeignKey(CakeCategory,on_delete=models.CASCADE)
    cake_name=models.CharField(max_length=200)
    options=(
        ('chocolate','chocolate'),
        ('black forest','black forest'),
        ('red velvet','red velvet'),
        ('butter  scotch','butter scotch'),
        ('vanilla','vanilla'),
        ('pineapple','pineapple'),
        ('dates','dates'),
        ('non-alcoholic','non-alcoholic'),
        ('dry-fruits','dry-fruits'),
        ('mixed-fruits','mixed-fruits'),
        ('blueberry','blueberry'),
        ('strawberry','strawberry')
    )
    flavours=models.CharField(max_length=200,choices=options,default="chocolate")
    image=models.ImageField(upload_to='images')

    @property
    def varients(self):
        qs=self.cakevarients_set.all()
        return qs
    @property
    def cakereview(self):
        qs=self.cakereview_set.all()
        return qs
    
    @property
    def avg_rating(self):
        ratings=self.cakereview_set.all().values_list("rating",flat=True)
        return sum(ratings)/len(ratings) if ratings else 0


    def __str__(self):
        return self.cake_name
    
# ----------------------Cake Varient Model--------------------------------

class CakeVarients(models.Model):
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE)
    cake_price=models.PositiveIntegerField()
    options=(
        ('0.5 kg','0.5 kg'),
        ('1 kg','1 kg'),
        ('2 kg','2 kg'),
        ('3 kg','3 kg'),
        ('4 kg','4 kg'),
        ('5 kg','5 kg')
    )
    weight=models.CharField(max_length=200,choices=options,default='0.5 kg')
    option=(
        ('egg','egg'),
        ('egg-less','egg-less')
    )
    cake_type=models.CharField(max_length=200,choices=option,default='egg')

    def __str__(self):
        return self.cake.cake_name
    
    @property
    def offers(self):
        current_date=date.today()
        qs=self.cakeoffers_set.all()
        qs=qs.filter(end_date__gte=current_date)
        return qs


# ----------------------Offer Model---------------------------------------

class CakeOffers(models.Model):
    cake_varient=models.ForeignKey(CakeVarients,on_delete=models.CASCADE)
    discount_price=models.PositiveIntegerField()
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()


# ----------------------Cart Model----------------------------------------

class CakeCart(models.Model):
    cake_varient=models.ForeignKey(CakeVarients,on_delete=models.DO_NOTHING)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ('in-cart','in-cart'),
        ('order-placed','order-placed'),
        ('cancelled','cancelled')
    )
    status=models.CharField(max_length=200,choices=options,default='in-cart')
    date=models.DateTimeField(auto_now_add=True)


# ----------------------Order Model---------------------------------------

class CakeOrders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cake_varient=models.ForeignKey(CakeVarients,on_delete=models.CASCADE)
    options=(
        ('order-placed','order-placed'),
        ('cancelled','cancelled'),
        ('packed','packed'),
        ('in-transit','in-transit'),
        ('delivered','delivered')
    )
    status=models.CharField(max_length=200,choices=options,default='order-placed')
    ordered_date=models.DateTimeField(auto_now_add=True)
    expected_date=models.DateField(null=True)
    address=models.CharField(max_length=200)


# -----------------------Review Model-------------------------------------

class CakeReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cake=models.ForeignKey(Cake,null=True,on_delete=models.SET_NULL)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=200)


