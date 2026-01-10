from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.EquipmentDashboardView.as_view(), name='dashboard'),
    
    # Equipment
    path('equipment/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment_detail'),
    path('equipment/create/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('equipment/<int:pk>/edit/', views.EquipmentUpdateView.as_view(), name='equipment_edit'),
    path('equipment/<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment_delete'),
    
    # Directorates
    path('directorates/', views.DirectorateListView.as_view(), name='directorate_list'),
    path('directorates/create/', views.DirectorateCreateView.as_view(), name='directorate_create'),
    path('directorates/<int:pk>/edit/', views.DirectorateUpdateView.as_view(), name='directorate_edit'),
    path('directorates/<int:pk>/delete/', views.DirectorateDeleteView.as_view(), name='directorate_delete'),
    
    # Assignments
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/create/', views.AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<int:pk>/return/', views.AssignmentReturnView.as_view(), name='assignment_return'),
    
    # Issues
    path('issues/', views.IssueListView.as_view(), name='issue_list'),
    path('issues/create/', views.IssueCreateView.as_view(), name='issue_create'),
    path('issues/<int:pk>/', views.IssueDetailView.as_view(), name='issue_detail'),
    path('issues/<int:pk>/resolve/', views.IssueResolveView.as_view(), name='issue_resolve'),
]

