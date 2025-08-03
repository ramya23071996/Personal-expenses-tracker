"""
URL configuration for Expenses_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tracker import views as tracker_views

urlpatterns = [
    path('admin/', admin.site.urls),

     path('', include('tracker.urls')),
path('register/', tracker_views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Tracker App
    path('', tracker_views.dashboard, name='dashboard'),
    path('expenses/', tracker_views.expense_list, name='expense_list'),
    path('expenses/add/', tracker_views.add_expense, name='add_expense'),
    path('expenses/edit/<int:pk>/', tracker_views.edit_expense, name='edit_expense'),
    path('expenses/delete/<int:pk>/', tracker_views.delete_expense, name='delete_expense'),

    path('accounts/', include('django.contrib.auth.urls')),
]
