"""
URL configuration for linkchecker_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from checker import views
from checker.api import api
from checker.views import home, dashboard, signup, export_csv, export_json
from django.contrib.auth import views as auth_views
from checker.views import monitor_page, get_url_data
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('', home),
    path('dashboard/', dashboard),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', signup),

    path('export/csv/', export_csv),
    path('export/json/', export_json),
    path('accounts/', include('allauth.urls')),
    path('monitor/', monitor_page),
    path('api/monitor-data/', get_url_data),
    path('login/', auth_views.LoginView.as_view(
    template_name='login.html',
    redirect_authenticated_user=True
), name='login'),
    path('export/cloud/', views.export_csv_cloud),
    path('reports/', views.reports_page),
    path('report/view/<int:report_id>/', views.view_report),
    path('report/delete/<int:report_id>/', views.delete_report),
    path('logout/', LogoutView.as_view(), name='logout'),   
]