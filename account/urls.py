from django.urls import path
from .views import profile_view, login_view, logout_view
app_name = 'account'
urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
