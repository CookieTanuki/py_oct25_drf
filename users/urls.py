from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

app_name = "users"

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [path('token-auth/', views.obtain_auth_token)]
urlpatterns += router.urls
