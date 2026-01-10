from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('<int:task_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:task_id>/attachment/', views.add_attachment, name='add_attachment'),
    path('<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
    path('<int:task_id>/complete/', views.task_complete, name='task_complete'),
    path('report-request/', views.report_request, name='report_request'),
    path('export/', views.task_export, name='task_export'),
]
