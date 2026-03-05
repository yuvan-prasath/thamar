from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('',views.splash,name="splash"),
    path('home/',views.home,name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('elder_request/', views.elder_request, name='elder_request'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/volunteers/', views.pending_volunteers, name='pending_volunteers'),
    path('staff/volunteer/<int:pk>/approve/', views.approve_volunteer, name='approve_volunteer'),
    path('staff/volunteer/<int:pk>/reject/', views.reject_volunteer, name='reject_volunteer'),

]
