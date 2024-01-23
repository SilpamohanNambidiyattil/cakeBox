from django.urls import path

from cakehouse.views import SignUpView,SignInView,CakeCategoryAddView,remove_categories,\
    CakeCreateView,CakeListView,CakeUpdateView,remove_cake,\
        CakeVarientsAddView,CakeDetailView,CakeVarientUpdateView,remove_cake_varient,\
        OffersAddView,remove_offers,IndexView,sign_out_view


urlpatterns=[
    path('register/',SignUpView.as_view(),name='signup'),
    path('',SignInView.as_view(),name='signin'),
    path('categories/add',CakeCategoryAddView.as_view(),name='cat-add'),
    path('categories/<int:pk>/remove',remove_categories,name='cat-remove'),
    path('cake/add',CakeCreateView.as_view(),name='cake-add'),
    path('cake/all',CakeListView.as_view(),name='cakes-list'),
    path('cake/<int:pk>/change',CakeUpdateView.as_view(),name='cake-change'),
    path('cake/<int:pk>/remove',remove_cake,name='cake-remove'),
    path('cake/<int:pk>/varients/add',CakeVarientsAddView.as_view(),name='cake-varients-add'),
    path('cake/<int:pk>',CakeDetailView.as_view(),name='cake-detail'),
    path('varients/<int:pk>/change',CakeVarientUpdateView.as_view(),name='cake-varient-change'),
    path('varient/<int:pk>/remove',remove_cake_varient,name='cake-varient-remove'),
    path('cakevarients/<int:pk>/offers/add',OffersAddView.as_view(),name='offers-add'),
    path('offers/<int:pk>/remove',remove_offers,name='offer-remove'),
    path('logout/',sign_out_view,name='signout'),
    path('index/',IndexView.as_view(),name='index')


]