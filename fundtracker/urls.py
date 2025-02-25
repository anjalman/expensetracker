"""
URL configuration for fundtracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SighnupView.as_view(),name="register"),
    path('sighnin/',views.SighInView.as_view(),name="sighnin"),
    path('index/',views.IndexView.as_view(),name="index"),
    path('sighnout/',views.sighnoutView.as_view(),name="sighnout"),
    path('expense/add/',views.ExpenseCreateView.as_view(),name="expense-add"),
    path('expense/<int:pk>/remove/',views.ExpenseDeleteView.as_view(),name="expense-delete"),
    path('expense/<int:pk>/change/',views.ExpenseUpdateVIew.as_view(),name="expense-update")
    
]
