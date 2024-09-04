from django.urls import path
from fpd import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from . import views
from .views import contact_view, success_view
from django.conf import settings


urlpatterns = [
    path('', views.index, name='Home'),
    path('about/', views.about, name='About'),
    path('contact/', contact_view, name='contact'),
    path('success/', success_view, name='success'),    
    path('learnmore/', views.learnmore, name='learnmore'),
    path('prediction', views.prediction, name='Prediction'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Correct logout view
]
