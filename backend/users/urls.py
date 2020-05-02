"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   25.04.2020 19:38
"""
from django.urls import path

from users import views

urlpatterns = [
    path('users/signup/', views.SignUpView.as_view(), name='user-sign-up'),
    path('users/signin/', views.SignInView.as_view(), name='user-sign-in'),
    path('users/signout/', views.SignOutView.as_view(), name='user-logout'),
    path('users/password-reset-requests/', views.PasswordResetRequestCreateView.as_view(), name='password-reset-email'),
    path('users/password-reset-requests/<str:token>/', views.PasswordResetRequestRetrieveView.as_view(),
         name='password-reset-check-token'),
    path('users/password-reset-confirmation/', views.PasswordResetConfirmationView.as_view(),
         name='password-reset-confirmation')
]
