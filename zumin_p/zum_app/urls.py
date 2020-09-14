from django.urls import path     
from . import views

urlpatterns = [
#RENDER  
    path('', views.index),
    path('welcome/<int:id>', views.welcome),
    path('user/<int:id>', views.one_user),
    path('tenant/<int:id>', views.tenant),
    path ('one_prop/<int:id>', views.one_prop),
    path ('tenant_oneprop/<int:id>', views.tenant_oneprop),
    path ('edit_profile/<int:id>', views.edit_prof),
    path ('profile/<int:id>', views.profile),


#REGITRATION
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
#Methods
   path('new_prop', views.new_prop),
   path('search', views.search),
   path('post', views.post),
   path('delete_prop/<int:id>', views.delete_prop),
   path('apply_prop/<int:id>', views.apply_prop),
]