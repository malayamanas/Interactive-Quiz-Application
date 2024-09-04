from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'quiz'

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register_view, name='register'),  # Registration page
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('quiz/', views.quiz_view, name='quiz'),  # Quiz page
    path('results/<int:score>/<int:total>/', views.results_view, name='results'),  # Results page

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
