import uuid
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import Student


# Create your models here.


class AcademicYear(models.Model):
    academic_year = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.academic_year


class Evaluation(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    facilitator = models.ForeignKey('Facilitator', on_delete=models.CASCADE)
    course = models.OneToOneField('Course', on_delete=models.CASCADE)
    description = models.CharField(max_length=150, blank=True, null=True)
    aggregated_score_computed_value = models.FloatField(default=0, editable=False)
    slug = models.SlugField(unique=True, default=uuid.uuid4)
    deadline = models.DateTimeField(null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Evaluation Reports'

    @property
    def check_active_status(self):
        if self.deadline > timezone.now():
            return True
        else:
            return False

    def __str__(self):
        return f"{self.course.course_code} - {self.course.name} - {self.course.course_group.upper()[0:1]}- {self.course.program} "

    def save(self, *args, **kwargs):
        # slug_value = self.course.name + '-' + str(self.facilitator.staff_id) + '-' + self.course.course_group
        # self.slug = slugify(slug_value)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('evaluation_report', kwargs={'slug': self.slug})


class EvaluationSubmission(models.Model):
    class FeedbackChoices(models.IntegerChoices):
        NOT_APPLICABLE = 0
        STRONGLY_DISAGREE = 1
        DISAGREE = 2
        MODERATELY_DISAGREE = 3
        AGREE = 4
        STRONGLY_AGREE = 5

    evaluationInfo = models.ForeignKey(Evaluation, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='submitted_evaluations')

    curriculum_feedback_beginning_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    curriculum_feedback_course_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    curriculum_feedback_lecture_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    curriculum_feedback_outcomes_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    curriculum_feedback_procedures_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    curriculum_feedback_books_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    attendance_schedule = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    attendance_punctuality = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    attendance_presence = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    delivery_enthusiasm = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_sequence = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_organization = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_clarity = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_contents = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_responsiveness = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_achievements = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_innovation = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_theory_practices = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    assignments_relevance = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    assignments_promptitude = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    assignments_feedback = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    assignments_guidance = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    interaction_availability = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    interaction_help = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    interaction_fairness = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    environment_classroom_size = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_seats = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_audio_visual_equip = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_public_address = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_books = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_computers = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_internet = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_air_conditioning = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_secretariat = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    slug = models.SlugField(unique=True, default=uuid.uuid4)
    submitter = models.ForeignKey(Student, blank=True, null=True, on_delete=models.PROTECT)
    is_evaluated = models.BooleanField(blank=False, null=False, default=False)

    # deadline = models.DateTimeField(null=False,blank=False, default=datetime.datetime)

    def __str__(self):
        return f"{self.evaluationInfo} {self.submitter}"

    def save(self, *args, **kwargs):
        # self.slug = str(self.evaluationInfo) + '-' + str(uuid.uuid4())
        # self.slug = slugify(self.slug[50:])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('evaluation', args=[self.slug])

    class Meta:
        unique_together = [('submitter', 'evaluationInfo')]


# Organisation Models
class Facilitator(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    staff_id = models.IntegerField(default=0)
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + str(self.staff_id) + ")"


class School(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=250)
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_department', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=250)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_program', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Course(models.Model):
    choices = (
        ('100', 'Level 100'),
        ('200', 'Level 200'),
        ('300', 'Level 300'),
        ('400', 'Level 400'),
        ('500', 'Level 500'),
        ('600', 'Level 600'),
        ('700', 'Level 700'),
        ('800', 'Level 800'),
    )

    lecture_group = (
        ('day', 'Day'),
        ('evening', 'Evening'),
        ('weekend', 'Weekend'),
    )

    name = models.CharField(max_length=250)
    course_code = models.CharField(max_length=10)
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    level = models.CharField(default='', max_length=15, choices=choices)
    course_group = models.CharField(default='', max_length=15, choices=lecture_group)
    facilitator = models.ForeignKey('Facilitator', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, default=uuid.uuid4)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name + " " + self.course_code + " (" + str(self.level) + ")" + '–' + self.course_group.upper()[
                                                                                         0:1] + '-' + str(self.program)

    def get_absolute_url(self):
        return reverse('view_course', kwargs={'slug': self.slug})

    # def clean(self):
    #     exists = Course.objects.filter(name=self.name, level=self.level, course_group=self.course_group,
    #                                    facilitator=self.facilitator)
    #     # slug_value = self.name + '-' + str(self.course_group) + '-' + str(uuid.uuid4())
    #
    #     if exists:
    #         raise ValidationError({'name': "Course with same specific details exists"})

    def save(self, *args, **kwargs):
        # try:

        count: int = 0
        self.full_clean()
        # slug_value = self.name + '-' + str(self.course_group) + '-' + str(self.program)[:10]
        # print(slug_value)
        # self.slug = slugify(slug_value)
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = [('name', 'level','course_group', 'facilitator','program')]