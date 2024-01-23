from django.shortcuts import render

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions

from cakehouse.models import Cake,CakeVarients,CakeCart,CakeOrders,CakeReview

from api.serializers import UserSerializer,CakeVarients,CakesSerializer,CartSerializer,OrderSerializer,ReviewSerializer

# Create your views here.

class UserCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
class CakesView(ModelViewSet):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CakesSerializer
    model=Cake
    queryset=Cake.objects.all()
    #custom method
    
    @action(methods=["post"],detail=True)
    def cart_add(self,request,*args,**kwargs):
        vid=kwargs.get("pk")
        varient_obj=CakeVarients.objects.get(id=vid)
        user=request.user
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cake_varient=varient_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # # url:http://127.0.0.1:8000/api/cloths/{varient_id}/place_order/    
    @action(methods=["post"],detail=True)
    def place_order(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        varient_object=CakeVarients.objects.get(id=id)
        user=request.user
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cake_varient=varient_object,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    # http://127.0.0.1:8000/api/cakes/{cakes_id}/add_review/
    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        c_id=kwargs.get("pk")
        cake_obj=Cake.objects.get(id=c_id)
        user=request.user
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cake=cake_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class CartsView(ViewSet):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CartSerializer

    def list(self,request,*args,**kwargs):
        qs=CakeCart.objects.filter(user=request.user)
        serializer=CartSerializer(qs,many=True) # deserialization
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance= CakeCart.objects.get(id=id)
        if instance.user==request.user:
            instance.delete()
            return Response(data={"msg":"deleted"})
        else:
            return Response(data={"msg":"permission denied"})
        
class OrdersView(ViewSet):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def list(self,request,*args,**kwargs):
        qs=CakeOrders.objects.filter(user=request.user)
        serializer=OrderSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=CakeOrders.objects.get(id=id)
        if instance.user==request.user:
            instance.delete()
            return Response(data={"msg":"removed"})
        else:
            return Response(data={"msg":"permission denied"})

class ReviewView(ViewSet):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ReviewSerializer
    def list(self,request,*args,**kwargs):
        qs=CakeReview.objects.filter(user=request.user)
        serializer=ReviewSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=CakeReview.objects.get(id=id)
        if instance.user==request.user:
            instance.delete()
            return Response(data={"msg":"deleted"})    
        else:
            return Response(data={"message":"permission denied"})