from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('',views.splash,name="splash"),
    path('home/',views.home,name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('elder_request/', views.elder_request, name='elder_request'),
]
