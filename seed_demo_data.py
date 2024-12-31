import os
import django
import random
from faker import Faker
from django.contrib.auth import get_user_model

import sys
# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_learning_platform.settings')

django.setup()

# Import your models
from users.models import CustomUser
from courses.models import Category, Course, Enrollment, Lesson, Comment, Review, CourseInstructor

# Initialize Faker instance
faker = Faker()

# Create CustomUsers
def create_users(n):
    for _ in range(n):
        username = faker.user_name()
        email = faker.email()
        password = faker.password()

        # Create a random role: 'instructor' or 'student'
        role = random.choice(['instructor', 'student'])
        is_instructor = role == 'instructor'
        is_student = role == 'student'
        is_active = True

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_instructor=is_instructor,
            is_student=is_student,
            is_active=is_active
        )
        print(f"Created user: {user.username} with role {role}")

# Create Categories
def create_categories(n):
    for _ in range(n):
        category_name = faker.word()
        description = faker.text(max_nb_chars=200)
        category = Category.objects.create(
            name=category_name,
            description=description
        )
        print(f"Created category: {category.name}")

# Create Courses
def create_courses(n):
    categories = Category.objects.all()
    for _ in range(n):
        course_title = faker.word() + " " + faker.word()
        image = faker.image_url()
        price = random.randint(10, 100)
        description = faker.text(max_nb_chars=200)
        category = random.choice(categories)
        course = Course.objects.create(
            title=course_title,
            description=description,
            category=category,
            price=price,
            image=image
        )
        print(f"Created course: {course.title} in category {category.name}")
        
# Create Lessons
def create_lessons(n):
    courses = Course.objects.all()
    for _ in range(n):
        course = random.choice(courses)
        lesson_title = faker.word() + " " + faker.word()
        video_url = faker.url()
        order = random.randint(1, 10)
        content = faker.text(max_nb_chars=200)
        lesson = Lesson.objects.create(
            course=course,
            title=lesson_title,
            description=content,
            video_url=video_url,
            order=order
        )
        print(f"Created lesson: {lesson.title} in course {course.title}")
        
# create course instructors
def create_course_instructors(n):
    instructors = CustomUser.objects.filter(is_instructor=True)
    courses = Course.objects.all()
    for _ in range(n):
        instructor = random.choice(instructors)
        course = random.choice(courses)
        course_instructor = CourseInstructor.objects.create(
            instructor=instructor,
            course=course
        )
        print(f"Created course instructor: {instructor.username} in course {course.title}")

# Create Enrollments for students
def create_enrollments(n):
    students = CustomUser.objects.filter(is_student=True)
    courses = Course.objects.all()
    lessons = Lesson.objects.all() 
    
    for _ in range(n):
        student = random.choice(students)
        course = random.choice(courses)
        
        # Create the enrollment
        enrollment = Enrollment.objects.create(
            student=student,
            course=course
        )
        
        # Randomly select lessons for the student to complete
        completed_lessons = random.sample(list(lessons), random.randint(1, 5))  # Choose 1-5 lessons
        enrollment.completed_lessons.set(completed_lessons)
        
        print(f"Created enrollment: {student.username} in course {course.title}")


# Create Comments for lessons
def create_comments(n):
    students = CustomUser.objects.filter(is_student=True)
    courses = Course.objects.all()
    content = faker.text(max_nb_chars=200)
    for _ in range(n):
        student = random.choice(students)
        course = random.choice(courses)
        comment = faker.text(max_nb_chars=200)
        comment = Comment.objects.create(
            student=student,
            course=course,
            comment=content
        )
        print(f"Created comment by {student.username} for lesson {course.title}")

# Create Reviews for courses
def create_reviews(n):
    students = CustomUser.objects.filter(is_student=True)
    courses = Course.objects.all()
    for _ in range(n):
        student = random.choice(students)
        course = random.choice(courses)
        rating = random.randint(1, 5)
        content = faker.text(max_nb_chars=200)
        review = Review.objects.create(
            student=student,
            course=course,
            rating=rating,
            review=content
        )
        print(f"Created review by {student.username} for course {course.title}")

        
# Clean up all data
def clean_data():
    CourseInstructor.objects.all().delete()
    Review.objects.all().delete()
    Comment.objects.all().delete()
    Enrollment.objects.all().delete()
    Lesson.objects.all().delete()
    Course.objects.all().delete()
    Category.objects.all().delete()
    CustomUser.objects.all().delete()
    
    print("All data deleted")

# Create data
def populate_data():
    
    clean_data()
    create_users(10)  
    create_categories(5) 
    create_courses(10)
    create_course_instructors(5)
    create_lessons(20) 
    create_enrollments(15)  
    create_comments(30) 
    create_reviews(20) 

populate_data()
