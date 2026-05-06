"""
URL configuration for bug_tracker_app project.

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
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/api/reporters/', create_new_reporter),
    path('/api/reporters/',get_all_reporters),
    path('/api/reporters/<id:int>',get_reporter_details),
    path('/api/issues/', create_new_issue),
    path('/api/issues/',get_all_issues),
    path('/api/issues/<id:int>',get_issue_details),
    path('/api/issues/<status:str>', get_filtered_issue_details)
]