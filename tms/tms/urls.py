"""
URL configuration for tms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from management_system import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ProjectView.as_view(), name="index"),
    path('signup/', views.register, name="signup"),
    path('login/', views.login_handler, name="login"),
    path('logout/', views.logout_handler, name="logout"),
    path('projects/', views.ProjectView.as_view(), name="projects"),
    path('project/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('project/delete/<int:pk>/', views.delete_project, name='project_del'),
    path('project/update/<int:pk>/', views.ProjectEditView.as_view(), name='project_update'),

    path('projects/<int:pk>/suits/', views.SuitView.as_view(), name="suits"),
    path('projects/<int:proj_id>/suit/', views.SuitCreateView.as_view(), name='suit_create'),
    path('projects/<int:proj_id>/suit/delete/<int:pk>/', views.delete_suit, name='suit_del'),
    path('projects/<int:proj_id>/suit/update/<int:pk>/', views.SuitEditView.as_view(), name='suit_update'),

    path('projects/<int:proj_id>/suit/<int:suit_id>/', views.TestCaseView.as_view(), name="test_cases"),
    path('projects/<int:proj_id>/suit/<int:suit_id>/tc/', views.TestCaseCreateView.as_view(), name="tc_create"),
    path('projects/<int:proj_id>/suit/<int:suit_id>/tc/<int:pk>/', views.TestCaseUpdate.as_view(), name="tc_update"),
    path('projects/<int:proj_id>/suit/<int:suit_id>/tc/delete/<int:pk>', views.delete_test_case, name="tc_delete"),
    path('projects/<int:proj_id>/suit/<int:suit_id>/tc_history/<int:pk>', views.TCHistoryView.as_view(), name="tc_history"),
    path('projects/<int:proj_id>/suit/<int:suit_id>/tc_history/<int:pk>/detail/', views.TCHistoryDetailView.as_view(), name="tc_history_detail"),
    path('projects/<int:proj_id>/suit/<int:suit_id>/tc_history/<int:tc_id>/recover/<int:pk>',
         views.recover_tc, name="tc_history_recover"),

    path('plans/', views.PlanView.as_view(), name="plans"),
    path('plan/create/', views.PlanCreateView.as_view(), name='plan_create'),
    path('plan/delete/<int:pk>/', views.delete_test_plan, name='plan_del'),
    path('plan/update/<int:pk>/', views.PlanEditView.as_view(), name='plan_update'),
]
