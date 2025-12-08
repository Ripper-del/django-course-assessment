from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')[:5]

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'

def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        course.users.add(request.user)
        return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))

def registration_request(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        try:
            User.objects.get(username=username)
            return render(request, 'onlinecourse/user_registration_bootstrap.html', {
                "message": "User already exists"
            })
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            user.save()
            login(request, user)
            return redirect('onlinecourse:index')
    return render(request, 'onlinecourse/user_registration_bootstrap.html')

def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            return render(request, 'onlinecourse/user_login_bootstrap.html', {"message": "Invalid login"})
    return render(request, 'onlinecourse/user_login_bootstrap.html')

def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')

def lesson_details(request, course_id, lesson_id):
    context = {}
    try:
        course = Course.objects.get(pk=course_id)
        lesson = Lesson.objects.get(pk=lesson_id)
        context['course'] = course
        context['lesson'] = lesson
    except:
        pass
    return render(request, "onlinecourse/lesson_detail.html", context)

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)

    choices = []
    for key in request.POST:
        if key.startswith('choice_'):
            choice_id = int(request.POST[key])
            choices.append(Choice.objects.get(id=choice_id))

    submission.choices.set(choices)
    submission_id = submission.id
    return HttpResponseRedirect(reverse(
        viewname='onlinecourse:exam_result', 
        args=(course_id, submission_id,)
    ))

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.get(id=submission_id)
    selected_choices = submission.choices.all()
    total_score = 0
    questions = course.question_set.all()
    
    for question in questions:
        correct_ids = set(choice.id for choice in question.choice_set.filter(is_correct=True))
        selected_ids = set(choice.id for choice in selected_choices if choice.question == question)
        if correct_ids == selected_ids and len(correct_ids) > 0:
            total_score += question.grade

    context['course'] = course
    context['grade'] = total_score
    context['questions'] = questions
    context['selected_choices'] = selected_choices
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)