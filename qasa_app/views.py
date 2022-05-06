from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, F, Avg, Sum, Max, Min, StdDev, Variance, Func
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
import requests

from accounts.auth_decorators import allowed_groups
from core.models import Evaluation, EvaluationSubmission, School, Department, AcademicYear, Program, Course, \
    Facilitator
# Create your views here.
from evaluation_project import settings
from qasa_app.forms import AcademicYearForm, SchoolForm, CreateDepartmentForm, CreateProgramForm, CreateCourseForm, \
    SetupEvaluationForm, AddFacilitatorForm

NUMBER_OF_CUMULATIVE_CHOICES = 6
NUMBER_OF_ATTENDANCE_CHOICES = 3
NUMBER_OF_DELIVERY_CHOICES = 9
NUMBER_OF_ASSIGNMENTS_CHOICES = 9
NUMBER_OF_INTERACTION_CHOICES = 3
NUMBER_OF_ENVIRONMENT_CHOICES = 9


# class Round(Func):
#     function = 'ROUND'
#     template = '%(function)s(%(expressions)s, 2)'


@allowed_groups(permitted_groups=['qasa'])
def analytic_dashboard(request):
    context = {
        'page_title': 'EV Analytic Dashboard',
    }
    return render(request, 'qasa_app/analysis/analytic_dashboard.html', context)


@allowed_groups(permitted_groups=['student'])
def student_dashboard(request):
    context = {
        'page_title': 'Analytic Dashboard',
    }
    return render(request, 'qasa_app/analysis/analytic_dashboard.html', context)


@allowed_groups(permitted_groups=['qasa'])
def setup_evaluation(request):
    form = SetupEvaluationForm()
    if request.method == 'POST':
        form = SetupEvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record saved successfully.")
            latest_course = Course.objects.latest('slug')
            return redirect('view_all_evaluations')
    context = {'form': form, 'page_title': 'Setup Evaluation'}
    return render(request, 'qasa_app/evaluation/setup_evaluation.html', context)


@allowed_groups(permitted_groups=['qasa'])
def view_all_evaluations(request):
    evaluations = Evaluation.objects.all()
    context = {
        'evaluations': evaluations
    }
    return render(request, 'qasa_app/evaluation/evaluations_list.html', context)


@allowed_groups(permitted_groups=['student', 'qasa'])
def view_evaluation(request, slug):
    evaluation = get_object_or_404(Evaluation, slug=slug)
    context = {'evaluation': evaluation}
    return render(request, 'qasa_app/evaluation/setup_evaluation.html', context)


@allowed_groups(permitted_groups=['qasa'])
def edit_evaluation(request, slug):
    evaluation = get_object_or_404(Evaluation, slug=slug)
    form = SetupEvaluationForm(instance=evaluation)
    if request.method == 'POST':
        form = SetupEvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record updated successfully.")
            latest_course = Course.objects.latest('slug')
            return redirect('view_all_evaluations')
    context = {'form': form}
    return render(request, 'qasa_app/evaluation/setup_evaluation.html', context)


@allowed_groups(permitted_groups=['qasa'])
def delete_evaluation(request, slug):
    found_evaluation = get_object_or_404(Evaluation, slug=slug)
    if request.method == 'POST':
        found_evaluation.delete()
        messages.success(request, f"Successfully deleted")
        return redirect('view_all_evaluations')
    return None


@allowed_groups(permitted_groups=['qasa'])
def evaluation_reports_generated_list(request):
    _reports = Evaluation.objects.all().annotate(submitted=Count(F('submitted_evaluations')))
    context = {
        'evaluation_reports': _reports,
        'page_title': 'Evaluation Reports'
    }
    return render(request, 'qasa_app/qasa_front.html', context)


@allowed_groups(permitted_groups=['qasa'])
def evaluation_report(request, slug):
    evaluation = get_object_or_404(Evaluation, slug=slug)
    evaluation_submitted = Evaluation.objects.filter(slug=slug).annotate(
        submitted=Count(F('submitted_evaluations'))).get()

    e_curriculum_feedback_beginning_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_beginning_answer')), Sum('curriculum_feedback_beginning_answer'),
                  Avg('curriculum_feedback_beginning_answer'),
                  Max(F('curriculum_feedback_beginning_answer')), Min(F('curriculum_feedback_beginning_answer')),
                  StdDev(F('curriculum_feedback_beginning_answer')),
                  Variance(F('curriculum_feedback_beginning_answer')),
                  )

    e_curriculum_feedback_course_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_course_answer')), Sum('curriculum_feedback_course_answer'),
                  Avg('curriculum_feedback_course_answer'),
                  Max(F('curriculum_feedback_course_answer')), Min(F('curriculum_feedback_course_answer')),
                  StdDev(F('curriculum_feedback_course_answer')),
                  Variance(F('curriculum_feedback_course_answer')),
                  )

    e_curriculum_feedback_lecture_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_lecture_answer')), Sum('curriculum_feedback_lecture_answer'),
                  Avg('curriculum_feedback_lecture_answer'),
                  Max(F('curriculum_feedback_lecture_answer')), Min(F('curriculum_feedback_lecture_answer')),
                  StdDev(F('curriculum_feedback_lecture_answer')),
                  Variance(F('curriculum_feedback_lecture_answer')),
                  )
    e_curriculum_feedback_outcomes_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_outcomes_answer')), Sum('curriculum_feedback_outcomes_answer'),
                  Avg('curriculum_feedback_outcomes_answer'),
                  Max(F('curriculum_feedback_outcomes_answer')), Min(F('curriculum_feedback_outcomes_answer')),
                  StdDev(F('curriculum_feedback_outcomes_answer')),
                  Variance(F('curriculum_feedback_outcomes_answer')),
                  )

    e_curriculum_feedback_procedures_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_procedures_answer')), Sum('curriculum_feedback_procedures_answer'),
                  Avg('curriculum_feedback_procedures_answer'),
                  Max(F('curriculum_feedback_procedures_answer')), Min(F('curriculum_feedback_procedures_answer')),
                  StdDev(F('curriculum_feedback_procedures_answer')),
                  Variance(F('curriculum_feedback_procedures_answer')),
                  )

    e_curriculum_feedback_books_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_books_answer')), Sum('curriculum_feedback_books_answer'),
                  Avg('curriculum_feedback_books_answer'),
                  Max(F('curriculum_feedback_books_answer')), Min(F('curriculum_feedback_books_answer')),
                  StdDev(F('curriculum_feedback_books_answer')),
                  Variance(F('curriculum_feedback_books_answer')),
                  )

    # Attendance
    attendance_schedule = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('attendance_schedule')), Sum('attendance_schedule'),
                  Avg('attendance_schedule'),
                  Max(F('attendance_schedule')), Min(F('attendance_schedule')),
                  StdDev(F('attendance_schedule')),
                  Variance(F('attendance_schedule')),
                  )

    attendance_punctuality = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('attendance_punctuality')), Sum('attendance_punctuality'),
                  Avg('attendance_punctuality'),
                  Max(F('attendance_punctuality')), Min(F('attendance_punctuality')),
                  StdDev(F('attendance_punctuality')),
                  Variance(F('attendance_punctuality')),
                  )

    attendance_presence = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('attendance_presence')), Sum('attendance_presence'),
                  Avg('attendance_presence'),
                  Max(F('attendance_presence')), Min(F('attendance_presence')),
                  StdDev(F('attendance_presence')),
                  Variance(F('attendance_presence')),
                  )

    # Delivery
    delivery_enthusiasm = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_enthusiasm')), Sum('delivery_enthusiasm'),
                  Avg('delivery_enthusiasm'),
                  Max(F('delivery_enthusiasm')), Min(F('delivery_enthusiasm')),
                  StdDev(F('delivery_enthusiasm')),
                  Variance(F('delivery_enthusiasm')),
                  )

    delivery_sequence = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_sequence')), Sum('delivery_sequence'),
                  Avg('delivery_sequence'),
                  Max(F('delivery_sequence')), Min(F('delivery_sequence')),
                  StdDev(F('delivery_sequence')),
                  Variance(F('delivery_sequence')),
                  )

    delivery_organization = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_organization')), Sum('delivery_organization'),
                  Avg('delivery_organization'),
                  Max(F('delivery_organization')), Min(F('delivery_organization')),
                  StdDev(F('delivery_organization')),
                  Variance(F('delivery_organization')),
                  )

    delivery_clarity = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_clarity')), Sum('delivery_clarity'),
                  Avg('delivery_clarity'),
                  Max(F('delivery_clarity')), Min(F('delivery_clarity')),
                  StdDev(F('delivery_clarity')),
                  Variance(F('delivery_clarity')),
                  )

    delivery_contents = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_contents')), Sum('delivery_contents'),
                  Avg('delivery_contents'),
                  Max(F('delivery_contents')), Min(F('delivery_contents')),
                  StdDev(F('delivery_contents')),
                  Variance(F('delivery_contents')),
                  )

    delivery_responsiveness = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_responsiveness')), Sum('delivery_responsiveness'),
                  Avg('delivery_responsiveness'),
                  Max(F('delivery_responsiveness')), Min(F('delivery_responsiveness')),
                  StdDev(F('delivery_responsiveness')),
                  Variance(F('delivery_responsiveness')),
                  )

    delivery_achievements = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_achievements')), Sum('delivery_achievements'),
                  Avg('delivery_achievements'),
                  Max(F('delivery_achievements')), Min(F('delivery_achievements')),
                  StdDev(F('delivery_achievements')),
                  Variance(F('delivery_achievements')),
                  )

    delivery_innovation = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_innovation')), Sum('delivery_innovation'),
                  Avg('delivery_innovation'),
                  Max(F('delivery_innovation')), Min(F('delivery_innovation')),
                  StdDev(F('delivery_innovation')),
                  Variance(F('delivery_innovation')),
                  )

    delivery_theory_practices = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_theory_practices')), Sum('delivery_theory_practices'),
                  Avg('delivery_theory_practices'),
                  Max(F('delivery_theory_practices')), Min(F('delivery_theory_practices')),
                  StdDev(F('delivery_theory_practices')),
                  Variance(F('delivery_theory_practices')),
                  )

    assignments_relevance = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('assignments_relevance')), Sum('assignments_relevance'),
                  Avg('assignments_relevance'),
                  Max(F('assignments_relevance')), Min(F('assignments_relevance')),
                  StdDev(F('assignments_relevance')),
                  Variance(F('assignments_relevance')),
                  )

    assignments_promptitude = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('assignments_promptitude')), Sum('assignments_promptitude'),
                  Avg('assignments_promptitude'),
                  Max(F('assignments_promptitude')), Min(F('assignments_promptitude')),
                  StdDev(F('assignments_promptitude')),
                  Variance(F('assignments_promptitude')),
                  )
    assignments_feedback = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('assignments_feedback')), Sum('assignments_feedback'),
                  Avg('assignments_feedback'),
                  Max(F('assignments_feedback')), Min(F('assignments_feedback')),
                  StdDev(F('assignments_feedback')),
                  Variance(F('assignments_feedback')),
                  )

    assignments_guidance = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('assignments_guidance')), Sum('assignments_guidance'),
                  Avg('assignments_guidance'),
                  Max(F('assignments_guidance')), Min(F('assignments_guidance')),
                  StdDev(F('assignments_guidance')),
                  Variance(F('assignments_guidance')),
                  )

    interaction_availability = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('interaction_availability')), Sum('interaction_availability'),
                  Avg('interaction_availability'),
                  Max(F('interaction_availability')), Min(F('interaction_availability')),
                  StdDev(F('interaction_availability')),
                  Variance(F('interaction_availability')),
                  )

    interaction_help = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('interaction_help')), Sum('interaction_help'),
                  Avg('interaction_help'),
                  Max(F('interaction_help')), Min(F('interaction_help')),
                  StdDev(F('interaction_help')),
                  Variance(F('interaction_help')),
                  )

    interaction_fairness = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('interaction_fairness')), Sum('interaction_fairness'),
                  Avg('interaction_fairness'),
                  Max(F('interaction_fairness')), Min(F('interaction_fairness')),
                  StdDev(F('interaction_fairness')),
                  Variance(F('interaction_fairness')),
                  )

    environment_classroom_size = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_classroom_size')), Sum('environment_classroom_size'),
                  Avg('environment_classroom_size'),
                  Max(F('environment_classroom_size')), Min(F('environment_classroom_size')),
                  StdDev(F('environment_classroom_size')),
                  Variance(F('environment_classroom_size')),
                  )

    environment_seats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_seats')), Sum('environment_seats'),
                  Avg('environment_seats'),
                  Max(F('environment_seats')), Min(F('environment_seats')),
                  StdDev(F('environment_seats')),
                  Variance(F('environment_seats')),
                  )

    environment_audio_visual_equip = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_audio_visual_equip')), Sum('environment_audio_visual_equip'),
                  Avg('environment_audio_visual_equip'),
                  Max(F('environment_audio_visual_equip')), Min(F('environment_audio_visual_equip')),
                  StdDev(F('environment_audio_visual_equip')),
                  Variance(F('environment_audio_visual_equip')),
                  )

    environment_public_address = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_public_address')), Sum('environment_public_address'),
                  Avg('environment_public_address'),
                  Max(F('environment_public_address')), Min(F('environment_public_address')),
                  StdDev(F('environment_public_address')),
                  Variance(F('environment_public_address')),
                  )

    environment_books = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_books')), Sum('environment_books'),
                  Avg('environment_books'),
                  Max(F('environment_books')), Min(F('environment_books')),
                  StdDev(F('environment_books')),
                  Variance(F('environment_books')),
                  )

    environment_computers = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_computers')), Sum('environment_computers'),
                  Avg('environment_computers'),
                  Max(F('environment_computers')), Min(F('environment_computers')),
                  StdDev(F('environment_computers')),
                  Variance(F('environment_computers')),
                  )

    environment_internet = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_internet')), Sum('environment_internet'),
                  Avg('environment_internet'),
                  Max(F('environment_internet')), Min(F('environment_internet')),
                  StdDev(F('environment_internet')),
                  Variance(F('environment_internet')),
                  )

    environment_air_conditioning = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_air_conditioning')), Sum('environment_air_conditioning'),
                  Avg('environment_air_conditioning'),
                  Max(F('environment_air_conditioning')), Min(F('environment_air_conditioning')),
                  StdDev(F('environment_air_conditioning')),
                  Variance(F('environment_air_conditioning')),
                  )

    environment_secretariat = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_secretariat')), Sum('environment_secretariat'),
                  Avg('environment_secretariat'),
                  Max(F('environment_secretariat')), Min(F('environment_secretariat')),
                  StdDev(F('environment_secretariat')),
                  Variance(F('environment_secretariat')),
                  )

    # print("cumulative_stats", cumulative_stats)
    # cumulative_sum_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
    #     .annotate(cumulative_sum_submission=(Sum(F('curriculum_feedback_beginning_answer')) +
    #                                          Sum(F('curriculum_feedback_course_answer')) +
    #                                          Sum(F('curriculum_feedback_lecture_answer')) +
    #                                          Sum(F('curriculum_feedback_outcomes_answer')) +
    #                                          Sum(F('curriculum_feedback_procedures_answer')) +
    #                                          Sum(F('curriculum_feedback_books_answer'))
    #                                          )) \
    #     .aggregate(Sum('cumulative_sum_submission'))

    # Statistical Averaging
    cumulative_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(cumulative_avg_submission=(Avg(F('curriculum_feedback_beginning_answer')) +
                                             Avg(F('curriculum_feedback_course_answer')) +
                                             Avg(F('curriculum_feedback_lecture_answer')) +
                                             Avg(F('curriculum_feedback_outcomes_answer')) +
                                             Avg(F('curriculum_feedback_procedures_answer')) +
                                             Avg(F('curriculum_feedback_books_answer'))
                                             )) \
        .aggregate((Avg('cumulative_avg_submission')))

    attendance_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(attendance_avg_submission=(Avg(F('attendance_schedule')) +
                                             Avg(F('attendance_punctuality')) +
                                             Avg(F('attendance_presence'))
                                             )) \
        .aggregate((Avg('attendance_avg_submission')))

    delivery_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(delivery_avg_submission=(Avg(F('delivery_enthusiasm')) +
                                           Avg(F('delivery_sequence')) +
                                           Avg(F('delivery_organization')) +
                                           Avg(F('delivery_clarity')) +
                                           Avg(F('delivery_contents')) +
                                           Avg(F('delivery_responsiveness')) +
                                           Avg(F('delivery_achievements')) +
                                           Avg(F('delivery_innovation')) +
                                           Avg(F('delivery_theory_practices'))
                                           )) \
        .aggregate((Avg('delivery_avg_submission')))

    assignments_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(assignments_avg_submission=(Avg(F('assignments_relevance')) +
                                              Avg(F('assignments_promptitude')) +
                                              Avg(F('assignments_feedback')) +
                                              Avg(F('assignments_guidance'))

                                              )) \
        .aggregate((Avg('assignments_avg_submission')))

    interaction_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(interaction_avg_submission=(Avg(F('interaction_availability')) +
                                              Avg(F('interaction_help')) +
                                              Avg(F('interaction_fairness'))

                                              )) \
        .aggregate((Avg('interaction_avg_submission')))

    environment_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(environment_avg_submission=(Avg(F('environment_classroom_size')) +
                                              Avg(F('environment_seats')) +
                                              Avg(F('environment_audio_visual_equip')) +
                                              Avg(F('environment_public_address')) +
                                              Avg(F('environment_books')) +
                                              Avg(F('environment_computers')) +
                                              Avg(F('environment_internet')) +
                                              Avg(F('environment_air_conditioning')) +
                                              Avg(F('environment_secretariat'))

                                              )) \
        .aggregate((Avg('environment_avg_submission')))

    averaged_cum_stats = round(
        float((cumulative_avg_stats['cumulative_avg_submission__avg']) / NUMBER_OF_CUMULATIVE_CHOICES), 2) if (
                                                                                                                  cumulative_avg_stats[
                                                                                                                      'cumulative_avg_submission__avg']) is not None else 0
    averaged_attendance_stats = round(
        float(attendance_avg_stats['attendance_avg_submission__avg']) / NUMBER_OF_ATTENDANCE_CHOICES, 2) if (
                                                                                                                attendance_avg_stats[
                                                                                                                    'attendance_avg_submission__avg']) is not None else 0
    averaged_delivery_stats = round(
        float(delivery_avg_stats['delivery_avg_submission__avg']) / NUMBER_OF_DELIVERY_CHOICES, 2) if (
                                                                                                          delivery_avg_stats[
                                                                                                              'delivery_avg_submission__avg']) is not None else 0
    averaged_assignments_stats = round(
        float(assignments_avg_stats['assignments_avg_submission__avg']) / NUMBER_OF_ASSIGNMENTS_CHOICES, 2) if (
                                                                                                                   assignments_avg_stats[
                                                                                                                       'assignments_avg_submission__avg']) is not None else 0

    averaged_interaction_stats = round(
        float(interaction_avg_stats['interaction_avg_submission__avg']) / NUMBER_OF_INTERACTION_CHOICES, 2) if (
                                                                                                                   interaction_avg_stats[
                                                                                                                       'interaction_avg_submission__avg']) is not None else 0
    averaged_environment_stats = round(
        float(environment_avg_stats['environment_avg_submission__avg']) / NUMBER_OF_ENVIRONMENT_CHOICES, 2) if (
                                                                                                                   environment_avg_stats[
                                                                                                                       'environment_avg_submission__avg']) is not None else 0
    total_score_cumulatively = round((
                                             averaged_cum_stats + averaged_attendance_stats + averaged_delivery_stats + averaged_assignments_stats + averaged_interaction_stats) / 5,
                                     2)
    context = {
        'evaluation': evaluation,
        'page_title': f"{evaluation_submitted} Report",
        'evaluation_submitted': evaluation_submitted,

        'averaged_cum_stats': averaged_cum_stats,
        'averaged_attendance_stats': averaged_attendance_stats,
        'averaged_delivery_stats': averaged_delivery_stats,
        'averaged_assignments_stats': averaged_assignments_stats,
        'averaged_interaction_stats': averaged_interaction_stats,
        'averaged_environment_stats': averaged_environment_stats,
        'total_score_cumulatively': total_score_cumulatively,

        'curriculum': {
            "beginning": e_curriculum_feedback_beginning_answer_stats,
            "course": e_curriculum_feedback_course_answer_stats,
            "lecture": e_curriculum_feedback_lecture_answer_stats,
            "outcomes": e_curriculum_feedback_outcomes_answer_stats,
            "procedures": e_curriculum_feedback_procedures_answer_stats,
            "books": e_curriculum_feedback_books_answer_stats,

        },

        'cumulative_avg_stats': cumulative_avg_stats,
        'attendance': {
            'schedule': attendance_schedule,
            'punctuality': attendance_punctuality,
            'presence': attendance_presence,
        },
        'delivery': {
            'enthusiasm': delivery_enthusiasm,
            'sequence': delivery_sequence,
            'organization': delivery_organization,
            'clarity': delivery_clarity,
            'contents': delivery_contents,
            'responsiveness': delivery_responsiveness,
            'achievements': delivery_achievements,
            'innovation': delivery_innovation,
            'theory practices': delivery_theory_practices
        },
        'assignments': {
            'relevance': assignments_relevance,
            'promptitude': assignments_promptitude,
            'feedback': assignments_feedback,
            'guidance': assignments_guidance
        },
        'interactions': {
            'availability': interaction_availability,
            'help': interaction_help,
            'fairness': interaction_fairness
        },

        'environment': {
            'classroom size': environment_classroom_size,
            'seats': environment_seats,
            'audio visual equip': environment_audio_visual_equip,
            'public address': environment_public_address,
            'books': environment_books,
            'computers': environment_computers,
            'internet': environment_internet,
            'environment air conditioning': environment_air_conditioning,
            'environment secretariat': environment_secretariat

        }
    }

    return render(request, 'qasa_app/evaluation_report.html', context)


@allowed_groups(permitted_groups=['qasa'])
def school_with_departments(request, slug):
    found_school = get_object_or_404(School, slug=slug)
    list_of_departments = Department.objects.filter(school=found_school)
    context = {'departments': list_of_departments}
    return render(request, 'qasa_app/department/departments.html', context)


# Academic Year Views

@allowed_groups(permitted_groups=['qasa'])
def view_academic_years(request):
    ayears = AcademicYear.objects.all()
    context = {'academic_years': ayears}
    return render(request, 'qasa_app/academic_year/academic_years.html', context)


@allowed_groups(permitted_groups=['qasa'])
def view_academic_year(request, pk):
    academic_year = get_object_or_404(AcademicYear, pk=pk)
    context = {'academic_year': academic_year}
    return render(request, 'qasa_app/academic_year/create_academic_year.html', context)


@allowed_groups(permitted_groups=['qasa'])
def create_academic_year(request):
    form = AcademicYearForm()
    if request.method == 'POST':
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_academic_years')
    context = {'form': form, }
    return render(request, 'qasa_app/academic_year/create_academic_year.html', context)


@allowed_groups(permitted_groups=['qasa'])
def delete_academic_year(request, pk):
    ayear = get_object_or_404(AcademicYear, pk=pk)
    if request.method == 'POST':
        ayear.delete()
        messages.success(request, f"Successfully deleted")
        return redirect('view_academic_years')
    return None


# School view functions
@allowed_groups(permitted_groups=['qasa'])
def view_schools(request):
    list_of_schools = School.objects.all().order_by('-name')
    context = {'schools': list_of_schools}
    return render(request, 'qasa_app/school/schools.html', context)


@allowed_groups(permitted_groups=['qasa'])
def create_school(request):
    form = SchoolForm()
    context = {'form': form}

    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record saved successfully.")
            return redirect('view_schools')
        else:
            form = SchoolForm(request.POST)
            context['errors'] = form.errors.as_json()
            return render(request, 'qasa_app/school/create_school.html', context)

    return render(request, 'qasa_app/school/create_school.html', context)


@allowed_groups(permitted_groups=['qasa'])
def school(request, slug):
    found_school = get_object_or_404(School, slug=slug)
    context = {'school': found_school}
    return render(request, 'qasa_app/school/school.html', context)


@allowed_groups(permitted_groups=['qasa'])
def edit_school(request, slug):
    found_school = get_object_or_404(School, slug=slug)
    form = SchoolForm(instance=found_school)
    if request.method == 'POST':
        form = SchoolForm(request.POST, instance=found_school)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record updated successfully.")
            return redirect('view_schools')
    context = {'form': form}
    return render(request, 'qasa_app/department/edit_department.html', context)


@allowed_groups(permitted_groups=['qasa'])
def delete_school(request, pk):
    found_school = get_object_or_404(School, pk=pk)
    if request.method == 'POST':
        found_school.delete()
        messages.success(request, f"Successfully deleted")
        return redirect('view_schools')
    return None


# department view functions
@allowed_groups(permitted_groups=['qasa'])
def view_department(request, slug):
    found_department = get_object_or_404(Department, slug=slug)
    context = {'department': found_department}
    return render(request, 'qasa_app/department/department.html', context)


@allowed_groups(permitted_groups=['qasa'])
def create_department(request):
    form = CreateDepartmentForm()
    if request.method == 'POST':
        form = CreateDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record saved successfully.")
            return redirect('view_schools')
    context = {'form': form}
    return render(request, 'qasa_app/department/create_department.html', context)


@allowed_groups(permitted_groups=['qasa'])
def edit_department(request, slug):
    department = get_object_or_404(Department, slug=slug)
    form = CreateDepartmentForm(instance=department)
    if request.method == 'POST':
        form = CreateDepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record updated successfully.")
            return redirect('school_with_departments', slug=department.school.slug)
    context = {'form': form}
    return render(request, 'qasa_app/department/edit_department.html', context)


@allowed_groups(permitted_groups=['qasa'])
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, f"Successfully deleted")
        return redirect('school_with_departments', slug=department.school.slug)
    return None


# Program view functions
@allowed_groups(permitted_groups=['qasa'])
def view_program(request, slug):
    found_program = get_object_or_404(Program, slug=slug)
    context = {'main_program': found_program}
    print("program=>", found_program)
    return render(request, 'qasa_app/program/program.html', context)


@allowed_groups(permitted_groups=['qasa'])
def create_program(request):
    form = CreateProgramForm()
    if request.method == 'POST':
        form = CreateProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record saved successfully.")
            return redirect('view_schools')
    context = {'form': form}
    return render(request, 'qasa_app/program/create_program.html', context)


@allowed_groups(permitted_groups=['qasa'])
def edit_program(request, slug):
    program = get_object_or_404(Program, slug=slug)
    form = CreateProgramForm(instance=program)
    if request.method == 'POST':
        form = CreateProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record updated successfully.")
            return redirect('view_department', slug=program.department.slug)
    context = {'form': form}
    return render(request, 'qasa_app/program/edit_program.html', context)


@allowed_groups(permitted_groups=['qasa'])
def delete_program(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        program.delete()
        messages.success(request, f"Successfully deleted")
        return redirect('view_schools')
    return None


@allowed_groups(permitted_groups=['qasa'])
def view_course(request, slug):
    found_course = get_object_or_404(Course, slug=slug)
    context = {'main_course': found_course}
    return render(request, 'qasa_app/course/course.html', context)


# Course view functions
@allowed_groups(permitted_groups=['qasa'])
def create_course(request):
    form = CreateCourseForm()
    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record saved successfully.")
            latest_course = Course.objects.latest('slug')
            return redirect('view_program', slug=latest_course.program.slug)
    context = {'form': form}
    return render(request, 'qasa_app/course/create_course.html', context)


@allowed_groups(permitted_groups=['qasa'])
def edit_course(request, slug):
    course = Course.objects.get(slug=slug)
    form = CreateCourseForm(instance=course)
    if request.method == 'POST':
        form = CreateCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record updated successfully.")
            return redirect('view_program', slug=course.program.slug)
    context = {'form': form, 'course': course}
    return render(request, 'qasa_app/course/edit_course.html', context)


@allowed_groups(permitted_groups=['qasa'])
def delete_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        course.delete()
        messages.success(request, f"Successfully deleted")
        return redirect('view_program', slug=course.program.slug)
    return None


# Facilitator view functions
@allowed_groups(permitted_groups=['qasa'])
def add_facilitator(request):
    form = AddFacilitatorForm()
    if request.method == 'POST':
        form = AddFacilitatorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record saved successfully.")

            return redirect('view_facilitators')
    context = {'form': form}
    return render(request, 'qasa_app/course/add_facilitator.html', context)


@allowed_groups(permitted_groups=['qasa'])
def edit_facilitator(request, pk):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    form = AddFacilitatorForm(instance=facilitator)
    if request.method == 'POST':
        form = AddFacilitatorForm(request.POST, instance=facilitator)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record updated successfully.")
            return redirect('view_facilitators')
    context = {'form': form}
    return render(request, 'qasa_app/course/edit_facilitator.html', context)


@allowed_groups(permitted_groups=['qasa'])
def delete_facilitator(request, pk):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    if request.method == 'POST':
        facilitator.delete()
        messages.success(request, f"Successfully deleted")
        return redirect('view_facilitators')
    return None


@allowed_groups(permitted_groups=['qasa'])
def view_facilitators(request):
    facilitators = Facilitator.objects.all()
    context = {'facilitators': facilitators}
    return render(request, 'qasa_app/course/facilitators.html', context)


def send_ux_email(request):
    if request.method == 'POST':
        send_simple_message()
        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     settings.EMAIL_HOST_USER,
        #     [request.user.email],
        #     fail_silently=False,
        # )

        messages.success(request, 'Message sent!')
        return redirect('evaluations')
    return None


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandboxabdcfdbf708c470296136ecfdf64ee27.mailgun.org/messages",
        auth=("api", "6c7a86de276949decfc38f15b160a393-62916a6c-c1476a4d"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxabdcfdbf708c470296136ecfdf64ee27.mailgun.org>",
              "to": "Raphael Amponsah <ralphvine2020@gmail.com>",
              "subject": "Hello Raphael Amponsah",
              "text": "Congratulations Raphael Amponsah, you just sent an email with Mailgun!  You are truly awesome!"}
    )

# You can see a record of this email in your logs: https://app.mailgun.com/app/logs.

# You can send up to 300 emails/day from this sandbox server.
# Next, you should add your own domain so you can send 10000 emails/month for free.