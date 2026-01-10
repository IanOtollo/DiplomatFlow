from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('task-analytics/', views.task_analytics, name='task_analytics'),
    path('team-performance/', views.team_performance, name='team_performance'),
    path('monthly-report/', views.monthly_report, name='monthly_report'),
    path('export-data/', views.export_data, name='export_data'),
]
