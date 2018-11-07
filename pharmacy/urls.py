"""pharmacy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import pharmadoc
from pharmadoc import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pharmadoc.views.start_view, name='startview'),
    path('submit/createsubmission', pharmadoc.views.createsubmission, name='createsubmission'),
    path('submit/<int:primary_key>', pharmadoc.views.submit_view, name='submitview'),
    path('submissions/<int:primary_key>', pharmadoc.views.seesubmissions, name='seesubmissions'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password/reset', pharmadoc.views.change_password, name='change_password'),
]
