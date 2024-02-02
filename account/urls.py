from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('sign-up/', register, name='sign-up'),
    path('profile/', profile_view, name='profile'),
]

