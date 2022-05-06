from cProfile import label

from django import forms
from .models import Evaluation, EvaluationSubmission


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = EvaluationSubmission
        fields = ["curriculum_feedback_beginning_answer",
                  'curriculum_feedback_course_answer',
                  'curriculum_feedback_lecture_answer',
                  'curriculum_feedback_outcomes_answer',
                  'curriculum_feedback_procedures_answer',
                  "curriculum_feedback_books_answer",

                  "attendance_schedule",
                  "attendance_punctuality",
                  "attendance_presence",

                  "delivery_enthusiasm",
                  "delivery_sequence",
                  "delivery_organization",
                  "delivery_clarity",
                  "delivery_contents",
                  "delivery_responsiveness",
                  "delivery_achievements",
                  "delivery_innovation",
                  "delivery_theory_practices",

                  "assignments_relevance",
                  "assignments_promptitude",
                  "assignments_feedback",
                  "assignments_guidance",

                  "interaction_availability",
                  "interaction_help",
                  "interaction_fairness",

                  "environment_classroom_size",
                  "environment_seats",
                  "environment_audio_visual_equip",
                  "environment_public_address",
                  "environment_books",
                  "environment_computers",
                  "environment_internet",
                  "environment_air_conditioning",
                  "environment_secretariat",

                  "is_evaluated",

                  # "submitter"

                  ]

        # def save(self, commit=True, *args, **kwargs):
        #     # obj = super(EvaluationForm, self).save(commit=False, *args, **kwargs)
        #     # print(f"{obj.curriculum_feedback_beginning} something good")
        #     if commit:
        #         obj.save()

        # class Meta:
        #     model = Evaluation
        #     fields = ['curriculum_feedback_beginning', 'curriculum_feedback_course', 'curriculum_feedback_lecture',
        #               'curriculum_feedback_procedures', 'curriculum_feedback_books']
        #
        widgets = {
            'curriculum_feedback_beginning_answer': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'curriculum_feedback_course_answer': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'curriculum_feedback_lecture_answer': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'curriculum_feedback_outcomes_answer': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'curriculum_feedback_procedures_answer': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'curriculum_feedback_books_answer': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),

            'attendance_schedule': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'attendance_punctuality': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'attendance_presence': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),

            'delivery_enthusiasm': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'delivery_sequence': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'delivery_organization': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'delivery_clarity': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'delivery_contents': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'delivery_responsiveness': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'delivery_achievements': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'delivery_innovation': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'delivery_theory_practices': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),

            'assignments_relevance': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'assignments_promptitude': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'assignments_feedback': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'assignments_guidance': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),

            'interaction_availability': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'interaction_help': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'interaction_fairness': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),

            'environment_classroom_size': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'environment_seats': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'environment_audio_visual_equip': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'environment_public_address': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'environment_books': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'environment_computers': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'environment_internet': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'environment_air_conditioning': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
            'environment_secretariat': forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
        }

        labels = {
            'curriculum_feedback_beginning_answer': 'The lecturer provided a detailed course outline at the beginning '
                                                    'of the course. ',
            'curriculum_feedback_course_answer': 'The lecturer clearly communicated the objectives of the course.',
            'curriculum_feedback_lecture_answer': 'The lecturer clearly communicated the objectives of each lecture.',
            'curriculum_feedback_outcomes_answer': 'The lecturer indicated the learning outcomes of the course at '
                                                   'the beginning of the course.',
            'curriculum_feedback_procedures_answer': 'The lecturer stated clearly the procedures by which students '
                                                     'will be assessed.',
            'curriculum_feedback_books_answer': 'Relevant recommended text books and other reference lists were ',

            'attendance_schedule': 'Most of the lectures took place as scheduled.',
            'attendance_punctuality': 'The lecturer was punctual for most of the lectures.',
            'attendance_presence': 'The lecturer was present for the entire scheduled periods.',

            'delivery_enthusiasm': 'The lecturer was enthusiastic about teaching and aroused my curiosity.',
            'delivery_sequence': 'The sequence of lectures followed the course outline provided.',
            'delivery_organization': 'Each lecture was presented in a well organized and structured manner.',
            'delivery_clarity': 'The material presented by the lecturer was always clearly explained.',
            'delivery_contents': 'The course content was thoroughly and adequately covered.',
            'delivery_responsiveness': 'The lecturer encouraged student participation and provided useful responses '
                                       'to questions.',
            'delivery_achievements': 'Learning outcomes indicated at the beginning of the course were achieved.',
            'delivery_innovation': 'The lecturer used innovative teaching methods(cases, ICT, videos, field trips, '
                                   'role-pay).',
            'delivery_theory_practices': 'The course was taught in a manner that relates theory to practice.',

            'assignments_relevance': 'The lecturer provided relevant assignments at regular intervals.',
            'assignments_promptitude': 'Assignments were promptly marked and returned.',
            'assignments_feedback': 'Useful feedback and comments on the assignment were always provided.',
            'assignments_guidance': 'The lecturer provided effective supervision and guidance.',

            'interaction_availability': 'The lecturer was available during stated office hours to be consulted by '
                                        'students.',
            'interaction_help': 'The lecturer made an effort to help individual students who had difficulties with '
                                'the course.',
            'interaction_fairness': 'The lecturer was fair to, and respected the students.',

            'environment_classroom_size': 'The classroom with respect to the class size was comfortable.',
            'environment_seats': 'TThe seats in the classroom were comfortable.',
            'environment_audio_visual_equip': 'Audio and visual equipment were always available.',
            'environment_public_address': 'The public address system was always available.',
            'environment_books': 'The relevant books and journals are available in the library.',
            'environment_computers': 'The computer laboratory equipment were always available.',
            'environment_internet': 'Internet facility was always available.',
            'environment_air_conditioning': 'The air conditioning and ventilation were adequate.',
            'environment_secretariat': 'The overall performance of the Secretariat was good.',

            'is_evaluated': 'Confirm your evaluation'

        }