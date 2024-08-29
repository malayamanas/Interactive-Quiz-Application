from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_view, name='quiz'),
    path('results/<int:score>/<int:total>/', views.results_view, name='results'),
]
