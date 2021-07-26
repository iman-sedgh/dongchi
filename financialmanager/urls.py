from django.contrib import admin
from django.urls import path, include
from .views import deposit_view, withdraw_view, box_view, home_view, box_settings, box_creation, box_join
from django.conf import settings
from django.conf.urls.static import static
app_name = 'financialmanager'
urlpatterns = [
    path('api/incoming/', deposit_view),
    path('withdraw/', withdraw_view, name='withdraw_api'),
    path('box/', box_view, name='box_select'),
    path('box/boxsettings/', box_settings, name='boxsettings'),
    path('box/boxcreation/', box_creation, name='boxcreation'),
    path('box/join/<uuid:inviteid>', box_join, name='boxjoin'),
    path('box/<slug:boxslug>/', box_view, name='box'),
    path('', home_view, name='home'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
