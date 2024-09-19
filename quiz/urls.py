from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'quiz'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('results/<int:score>/<int:total>/', views.results_view, name='results'),

    # Password reset paths
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/resetpassword.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Other quiz-related paths
    path('start/', views.quiz_start, name='start'),
    path('previous-results/', views.previous_results_view, name='previous_results'),
    path('profile/', views.view_profile, name='profile'),
    path('userhome/', views.user_home, name='user_home'),
]
