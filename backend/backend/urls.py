from django.contrib import admin
from django.urls import path, re_path, include
from django.shortcuts import render




def render_react(request):
    print("INDEX")
    return render(request, "index.html")

  
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
    path('', render_react),
]