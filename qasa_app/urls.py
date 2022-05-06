from django.urls import path

from .views import evaluation_reports_generated_list, view_schools, evaluation_report, view_academic_years, \
    create_academic_year, create_school, delete_academic_year, delete_school, school_with_departments, \
    create_department, delete_department, view_department, view_program, view_course, create_program, create_course, \
    edit_course, delete_course, edit_department, setup_evaluation, analytic_dashboard, view_all_evaluations, \
    edit_school, edit_program, delete_evaluation, edit_evaluation, student_dashboard, add_facilitator, edit_facilitator, \
    delete_facilitator, view_facilitators

urlpatterns = [



    path('dashboard/', analytic_dashboard, name='analytic_dashboard'),

    path('courses/', create_course, name='create_course'),
    path('courses/<slug:slug>/', view_course, name='view_course'),
    path('courses/<slug:slug>/edit', edit_course, name='edit_course'),
    path('courses/<slug:slug>/delete', delete_course, name='delete_course'),

    path('programs/<slug:slug>/', view_program, name='view_program'),
    path('programs/<slug:slug>/edit', edit_program, name='edit_program'),
    path('programs/create', create_program, name='create_program'),

    path('departments/<slug:slug>/', view_department, name='view_department'),
    path('departments/create', create_department, name='create_department'),
    path('department/<int:pk>/delete', delete_department, name='delete_department'),
    path('departments/<slug:slug>/edit', edit_department, name='edit_department'),

    path('facilitators/', view_facilitators, name='view_facilitators'),
    path('facilitators/create', add_facilitator, name='add_facilitator'),
    path('facilitators/<int:pk>/edit', edit_facilitator, name='edit_facilitator'),
    path('facilitators/<int:pk>/delete', delete_facilitator, name='delete_facilitator'),

    path('academic-years/', view_academic_years, name='view_academic_years'),
    path('academic-years/<int:pk>', delete_academic_year, name='delete_academic_year'),
    path('academic-years/create/', create_academic_year, name='create_academic_year'),

    path('schools/', view_schools, name='view_schools'),
    path('schools/create/', create_school, name='create_school'),
    path('schools/<slug:slug>/edit/', edit_school, name='edit_school'),
    path('schools/<int:pk>/', delete_school, name='delete_school'),
    path('schools/<slug:slug>/', school_with_departments, name='school_with_departments'),

    path('evaluations/', view_all_evaluations, name='view_all_evaluations'),
    path('evaluation/setup/', setup_evaluation, name='setup_evaluation'),
    path('evaluation/report/', evaluation_reports_generated_list, name='evaluation_reports_generated_list'),
    path('evaluation/reports/<slug:slug>', evaluation_report, name='evaluation_report'),
    path('evaluation/<slug:slug>/delete', delete_evaluation, name='delete_evaluation'),
    path('evaluation/<slug:slug>/edit', edit_evaluation, name='edit_evaluation'),









]