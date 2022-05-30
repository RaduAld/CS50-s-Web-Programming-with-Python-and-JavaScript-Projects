from django.db import models
from django.contrib.auth.models import AbstractUser

class Roles(models.TextChoices):
    ST = 'ST'
    PT = 'PT'
    TC = 'TC'

class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    role = models.CharField(choices=Roles.choices, max_length=2, blank= False, default='ST')
    schclass = models.ForeignKey("Class_school", on_delete=models.SET_NULL, related_name="schoclass", blank=True, null=True)
    child = models.ForeignKey("User", on_delete=models.SET_NULL, related_name="parent", blank=True, null=True)

    REQUIRED_FIELDS = ('first_name', 'last_name', 'role')

    def __str__(self):
        return f"{self.id}. ({self.role}){self.username}"

class Class_school(models.Model):
    title = models.CharField(max_length=100)
    principal_teacher = models.ForeignKey("User", on_delete=models.CASCADE, related_name="class_teacher")
    students = models.ManyToManyField("User", related_name="class_students")
    subjects = models.ManyToManyField("Subject",  blank=True, related_name="class_subject")

    def __str__(self):
        return f"{self.id}. ({self.title})"

class Subject(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image = models.URLField(max_length=300)
    teacher = models.ForeignKey("User", on_delete=models.CASCADE, related_name="subject_teacher")
    originclass = models.ForeignKey("Class_school", on_delete=models.CASCADE, related_name="subject_class")

    def __str__(self):
        return f"{self.id}. {self.title}({self.originclass.title})"

class Grade(models.Model):
    grd_number = models.DecimalField(max_digits=3, decimal_places=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey("User", on_delete=models.CASCADE, related_name="grade_student")
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name="grade_subject")

    def __str__(self):
        return f"{self.id}. {self.grd_number}({self.student},{self.subject})"

class Homework(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name="homework_subject")
    start = models.DateField(auto_now_add=True)
    end = models.DateField()
    active = models.BooleanField()

    def __str__(self):
        return f"{self.id}. {self.title}({self.subject},{self.active})"

class Announcement(models.Model):
    text = models.CharField(max_length=500)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name="announcement_subject")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="announcement_origin")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}. {self.user.last_name} {self.user.first_name}({self.subject.title}) {self.text}"