from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('spendings.urls')),
    path('', include('custom_spendings.urls'))
]
