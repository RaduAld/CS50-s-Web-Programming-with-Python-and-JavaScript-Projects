import json
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from .models import User, Subject, Grade, Announcement, Homework, Class_school

# User
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "eduon/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "eduon/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "eduon/register.html", {
                "message": "Passwords must match."
            })

        # Ensure role is selected
        role = request.POST["role"]
        if role == 'PT':
            child_id = request.POST["student_id"]
            try:
                child = User.objects.get(id=child_id)
            except User.DoesNotExist:
                return render(request, "eduon/register.html", {
                    "message": "The entered student id is wrong."
                })
        else:
            child = None

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.role = role
            if role == 'PT':
                user.child = child
            user.save()
        except IntegrityError:
            return render(request, "eduon/register.html", {
                "message": "Email already logged in."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "eduon/register.html")

#student/Teacher/Parent
def classes_view(request):
    check_homework()
    if request.user.is_authenticated == False:
        return redirect("/login")
    try:
        if request.user.role == "ST":
            schclass = Class_school.objects.filter(students__username=request.user.username).first()
            subjects = schclass.subjects.all()
        elif request.user.role == "PT":
            student = request.user.child
            schclass = Class_school.objects.filter(students__username=student.username).first()
            subjects = schclass.subjects.all()
        elif request.user.role == "TC":
            subjects = Subject.objects.filter(teacher=request.user)
        subjects = subjects.order_by("title")
    except AttributeError:
        subjects = None
    return render(request, "eduon/index.html", {
        "subjects": subjects
    })

@csrf_exempt   
def class_view(request, class_id):
    subject = Subject.objects.get(id=class_id)
    schclass = subject.originclass
    students = schclass.students.order_by("last_name").all()
    text = 'You are not in the class you are trying to reach!'
    if request.user.role == 'ST':
        if request.user.schclass != schclass:
            return render(request, "eduon/error.html", {
                'text': text,
            })
    elif request.user.role == 'TC':
        if request.user != subject.teacher:
            return render(request, "eduon/error.html", {
                'text': text,
            })
    elif request.user.role == 'PT':
        if request.user.child.schclass != schclass:
            return render(request, "eduon/error.html", {
                'text': text,
            })
    check_homework()
    homework = Homework.objects.filter(subject=subject, active=True).all()
    announcements = Announcement.objects.filter(subject=subject).all()
    announcements = announcements.order_by("-timestamp").all()
    if request.user.role == 'ST':
        grades = Grade.objects.filter(student=request.user, subject=subject)
    elif request.user.role == 'TC':
        grades = Grade.objects.filter(subject=subject)
    elif request.user.role == 'PT':
        grades = Grade.objects.filter(student=request.user.child, subject=subject)
    if request.method == 'PUT':
        data = json.loads(request.body)
        mtd = data.get("mtd", "")
        if mtd == 'announcement':
            text = data.get("text", "")
            new = Announcement(text=text, subject=subject, user=request.user)
            new.save()
        elif mtd == 'homework':
            title = data.get("title", "")
            text = data.get("text", "")
            end = data.get("end", "")
            new = Homework(title=title, text=text,
                subject=subject,end=end, active=True)
            new.save()
        elif mtd == 'grade':
            grd_number = data.get("grade", "")
            student = data.get("student_id")
            student = User.objects.get(id=student)
            new = Grade(grd_number=grd_number,
                student=student, subject=subject)
            new.save()
        return JsonResponse({"message": "Put successful."}, status=201)
    return render(request, "eduon/class.html", {
        'subject': subject,
        'schclass': schclass,
        'students': students,
        'homework': homework,
        'announcements': announcements,
        'grades': grades
    })

def grades_view(request):
    try:
        if request.user.role == "PT":
            student = request.user.child
        else:
            student = request.user
        schclass = Class_school.objects.filter(students__username=student.username).first()
        subjects = schclass.subjects.all()
        grades = Grade.objects.filter(student=student)
    except AttributeError:
        subjects = None
        grades = None
    return render(request, "eduon/grades.html", {
        'subjects': subjects,
        'grades': grades
    })

def create_subject(request):
    schclasses = Class_school.objects.all()
    alert = False
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        schclass = request.POST["schclass"]
        schclass = Class_school.objects.get(id=schclass)
        image = request.POST["image"]
        new = Subject(title=title, description=description,
        image=image, teacher=request.user, originclass=schclass)
        new.save()
        schclass.subjects.add(new)
        schclass.save()
        alert = True
    return render(request, "eduon/create_subject.html", {
        "schclasses": schclasses,
        "alert": alert
    })

@csrf_exempt 
def your_class(request):
    if request.user.role != 'TC':
        text = 'You do not have permission to this site.'
        return render(request, "eduon/error.html", {
            'text': text,
        })
    if request.method == "PUT":
        data = json.loads(request.body)
        title = data.get("title", "")
        student_ids = data.get("students", "")
        students = User.objects.filter(id__in=student_ids).all()
        new = Class_school(title=title, principal_teacher=request.user)
        new.save()
        new.students.set(students)
        new.save()
        for student in students:
            student.schclass = new
            student.save()
        request.user.schclass = new
        request.user.schclass.save()
        return HttpResponseRedirect(reverse("your_class"))
    try:
        schclass = Class_school.objects.get(principal_teacher=request.user)
        subjects = schclass.subjects.order_by('title').all()
        students = schclass.students.order_by('last_name', 'first_name').all()
        grades = Grade.objects.filter(student__in=students).all()
        return render(request, "eduon/your_class.html", {
            'schclass': schclass,
            'subjects': subjects,
            'students': students,
            'grades': grades
        })
    except Class_school.DoesNotExist as den:
        fstudents = User.objects.filter(role='ST', schclass=None).all()
        fstudents = fstudents.order_by('last_name', 'first_name').all()
        return render(request, "eduon/create_class.html", {
            'students': fstudents
        })


# Check different status
def check_homework():
    homework = Homework.objects.all()
    present = datetime.now()
    present = present.date()
    for homework in homework:
        if homework.end < present:
            homework.active = False
            homework.save()
