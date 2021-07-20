from django.contrib import admin
from django.urls import path, include
from .views import deposit_view, withdraw_view, home
from django.conf import settings
from django.conf.urls.static import static
app_name = 'financialmanager'
urlpatterns = [
    path('api/incoming/', deposit_view),
    path('withdraw/', withdraw_view, name='withdraw_api'),
    path('', home, name='home')

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
