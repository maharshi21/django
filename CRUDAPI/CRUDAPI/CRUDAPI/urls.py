# myapp/urls.py


from django.urls import path, include

urlpatterns = [
    path('', include('myapp.urls')),
]
