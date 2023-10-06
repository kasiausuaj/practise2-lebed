from django.urls import path
from .views import (
    category_delete, 
    design_request_create, 
    design_request_delete, 
    design_request_detail, 
    design_request_edit, 
    design_request_list, 
    category_create, 
    category_detail, 
    category_edit, 
    category_list,
)

urlpatterns = [
    path('', design_request_list, name='request-home'),
    
    path('request/<int:pk>/', design_request_detail, name='design_request_detail'),
    path('request/new/', design_request_create, name='design_request_create'),
    path('request/<int:pk>/edit/', design_request_edit, name='design_request_edit'),
    path('request/<int:pk>/delete/', design_request_delete, name='design_request_delete'),
    path('request/', design_request_list, name='design_request_list'),
    path('request/<str:username>', design_request_list, name='design_request_list'),
    
    path('category/', category_list, name='category_list'),
    path('category/new/', category_create, name='category_create'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    
    path('category/<int:pk>/edit/', category_edit, name='category_edit'),
    path('category/<int:pk>/delete/', category_delete, name='category_delete'),
]