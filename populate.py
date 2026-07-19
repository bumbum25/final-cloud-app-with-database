import os
import django
from django.utils.timezone import now

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from onlinecourse.models import Course, Lesson, Instructor, Question, Choice

def populate():
    # Create or get Instructor
    instructor, created = Instructor.full_time = True, Instructor.objects.get_or_create(
        user_id=1,  # The admin user we created
        defaults={'full_time': True, 'total_learners': 0}
    )

    # 1. Create Python Course
    course, created = Course.objects.get_or_create(
        name="Introduction to Python",
        defaults={
            "description": "Learn the basics of Python programming, including data structures, syntax, and control flow.",
            "pub_date": now().date(),
            "image": "course_images/python.png"
        }
    )
    if created:
        course.instructors.add(instructor)
        print("Created Course: Introduction to Python")
    else:
        print("Course already exists")

    # 2. Create Lessons
    l1, created = Lesson.objects.get_or_create(
        course=course,
        title="Python Basics and Syntax",
        defaults={
            "order": 0,
            "content": "Python is an interpreted, high-level, general-purpose programming language. Learn about variables, syntax, indentation, and printing outputs."
        }
    )
    l2, created = Lesson.objects.get_or_create(
        course=course,
        title="Python Data Structures",
        defaults={
            "order": 1,
            "content": "Data structures allow you to organize and store data. Learn about mutable lists, immutable tuples, key-value dictionaries, and sets."
        }
    )

    # 3. Create Questions and Choices
    q1, created = Question.objects.get_or_create(
        question_text="Which of the following is a mutable data structure in Python?",
        defaults={"marks": 2.0}
    )
    if created:
        q1.courses.add(course)
        Choice.objects.create(question=q1, choice_text="List", is_correct=True)
        Choice.objects.create(question=q1, choice_text="Tuple", is_correct=False)
        Choice.objects.create(question=q1, choice_text="String", is_correct=False)
        Choice.objects.create(question=q1, choice_text="Integer", is_correct=False)
        print("Created Question 1 with Choices")

    q2, created = Question.objects.get_or_create(
        question_text="What is the correct syntax to output 'Hello World' in Python?",
        defaults={"marks": 1.0}
    )
    if created:
        q2.courses.add(course)
        Choice.objects.create(question=q2, choice_text="print('Hello World')", is_correct=True)
        Choice.objects.create(question=q2, choice_text="echo('Hello World')", is_correct=False)
        Choice.objects.create(question=q2, choice_text="p('Hello World')", is_correct=False)
        Choice.objects.create(question=q2, choice_text="printf('Hello World')", is_correct=False)
        print("Created Question 2 with Choices")

if __name__ == "__main__":
    populate()
