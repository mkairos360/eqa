from django.urls import path
from .views import evaluations, evaluation, edit_evaluation, evaluation_view_form

urlpatterns = [
    path('', evaluations, name='evaluations'),
    path('<slug:slug>/', evaluation, name='evaluation'),
    path('edit/<int:pk>/', edit_evaluation, name='edit_evaluation'),
    path('evaluate/<int:pk>/', evaluation_view_form, name='submit_evaluation'),
    # path('',views.EvaluationModuleView.as_view(),name='evaluation_module_view'),
    # path('<int:id>',views.EvaluationSingleView.as_view(),name='evaluation_single_view'),
]