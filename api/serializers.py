from rest_framework import serializers

from cakehouse.models import User,CakeVarients,Cake,CakeCart,CakeOrders,CakeReview,CakeOffers


class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["id","username","email","password","phone","address"]
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class OfferSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    discount_price=serializers.CharField(read_only=True)
    start_date=serializers.CharField(read_only=True)
    end_date=serializers.CharField(read_only=True)
    class Meta:
        model=CakeOffers
        exclude=("cake_varient",)
        
class CakeVarientSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    offers=OfferSerializer(many=True,read_only=True)
    class Meta:
        model=CakeVarients
        exclude=("cake",)
        # fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    cake=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=CakeReview
        fields="__all__"

class CakesSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField(read_only=True)
    # category=serializers.SlugRelatedField(read_only=True,slug_field="name")
    varients=CakeVarientSerializer(many=True,read_only=True)
    cakereview=ReviewSerializer(many=True,read_only=True)
    avg_rating=serializers.CharField(read_only=True)

    class Meta:
        model=Cake
        fields="__all__"   

class CartSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    cake_varient=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    class Meta:
        model=CakeCart
        fields=["id","cake_varient","user","status","date"]

class OrderSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    cake_varient=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    orderd_date=serializers.CharField(read_only=True)
    expected_date=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=CakeOrders
        fields="__all__"