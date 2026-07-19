from django.shortcuts import render
from django.http import HttpResponseRedirect
# Import any new Models here
from .models import Course, Enrollment, Question, Choice, Submission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                             password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)

def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')

def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled

# CourseListView
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))

# Submit view to create an exam submission record
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = get_object_or_404(Enrollment, user=user, course=course)
    
    if request.method == 'POST':
        # Create a submission object referring to the enrollment
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Collect the selected choices from exam form
        selected_choices = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choices.append(int(value))
        
        # Add each selected choice object to the submission object
        submission.choices.set(selected_choices)
        submission.save()
        
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    return redirect('onlinecourse:course_details', pk=course.id)

# Exam result view
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    questions = course.question_set.all()
    selected_choice_ids = [c.id for c in submission.choices.all()]
    
    total_score = 0
    total_marks = 0
    question_results = []
    
    for question in questions:
        total_marks += question.marks
        choices = question.choice_set.all()
        selected_choices_for_question = [c for c in choices if c.id in selected_choice_ids]
        
        is_correct = question.answered_correctly(selected_choice_ids)
        if is_correct:
            total_score += question.marks
            
        question_results.append({
            'question': question,
            'is_correct': is_correct,
            'selected_choices': selected_choices_for_question
        })
        
    if total_marks > 0:
        grade = (total_score / total_marks) * 100
    else:
        grade = 0
        
    context = {
        'course': course,
        'grade': grade,
        'submission': submission,
        'question_results': question_results
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
