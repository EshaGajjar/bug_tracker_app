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

from .views import (
    get_filtered_issue_details,
    get_issue_details,
    get_reporter_details,
    issues,
    reporters,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/reporters/", reporters),
    path("api/reporters/<int:id>/", get_reporter_details),
    path("api/issues/", issues),
    path("api/issues/<int:id>/", get_issue_details),
    path("api/issues/status/<str:status>/", get_filtered_issue_details),
]