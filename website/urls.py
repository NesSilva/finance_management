from django.contrib import admin
from django.urls import path, include

from accounts.views import login_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_view, name="login"),  
    path("/finance/", include("finance.urls")),
    path("accounts/", include("accounts.urls")),
]
