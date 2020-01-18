from django.urls import path
from . import views

app_name = 'profile'


urlpatterns = [
    path('update/info/', views.update_profile, name= 'edit'),
    path('<slug>/', views.profile_detail_view, name='detail')
]
