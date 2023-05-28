from django.urls import path
from . import views

from django.conf.urls import handler404
from .views import error_handler

app_name = 'management'

urlpatterns = [
    # Маршруты для администраторов
    path('admin-main/', views.admin_main, name='admin-main'),
    path('admin-managers/', views.admin_managers, name='admin-managers'),
    path('admin-employee/', views.admin_employee, name='admin-employee'),

    path('admin-manage/', views.admin_manage, name='admin-manage'),
    path('admin-requests/', views.admin_requests, name='admin-requests'),
    path('admin-subpro/', views.admin_submit_completion_request, name='admin-submit-project'),
    path('admin-subtask/', views.admin_submit_task_completion_request, name='admin-submit-task'),

    path('admin-projects/', views.admin_projects, name='admin-projects'),

    # Маршруты для менеджеров

    path('manager-main/', views.manager_main, name='manager-main'),
    path('manager-emploee/', views.manager_employee, name='manager-employee'),
    path('manager-manage/', views.manager_manage, name='manager-manage'),

    path('manager-manage-tasks/', views.manager_task_list, name='manager-task-list'),
    path('manager-manage-create-tasks/', views.manager_create_task, name='manager-task-create'),
    path('manager-main-delete-tasks/<int:task_id>/', views.manager_delete_task, name='manager-task-delete'),
    path('manager-main-update-tasks/<int:task_id>/', views.manager_update_task, name='manager-task-update'),

    path('manager-manage-create-project/', views.manager_create_project, name='manager-create-project'),

    # path('manager-submit-completion-request/', views.submit_completion_request, name='submit_completion_request'),

    path('add-employee-to-project/<int:project_id>/', views.add_employee_to_project, name='add_employee_to_project'),

    path('project/<int:project_id>/employee/<int:employee_id>/assign/', views.assign_employee_to_project,
         name='assign_employee_to_project'),

    # path('main-manager/', views.main_manager, name='main-manager'),

    # Маршруты для работников

    # path('main-employee/', views.main_employee, name='main-employee'),
    # path('main-manager/', views., name='main-manager'),
]

handler404 = error_handler
