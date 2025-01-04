from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Course, Enrollment, Lesson, Comment, Review, CourseInstructor
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from django.conf import settings
from users.models import CustomUser


# Home Page
def index(request):
    categories = Category.objects.order_by('-created_at')[:4]
    courses = Course.objects.annotate(
        enrolled=Count('enrollment')).order_by('-enrolled')[:4]

    # Round the rating to 2 decimal places for display
    for course in courses:
        course.rating = round(course.rating, 2) if hasattr(
            course, 'rating') else 0

    total_courses = Course.objects.count()
    total_categories = Category.objects.count()
    instructors = CustomUser.objects.filter(is_instructor=True)[:4]

    return render(request, 'courses/home.html', {
        'categories': categories,
        'courses': courses,
        'total_courses': total_courses,
        'total_categories': total_categories,
        'instructors': instructors,
    })


# about page
def about(request):
    return render(request, 'about.html')
# List Categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'courses/category_list.html', {'categories': categories})

# Category Detail (Courses by Category)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = Course.objects.filter(category=category)
    return render(request, 'courses/category_detail.html', {'category': category, 'courses': courses})

# List Courses
def course_list(request):
    category_filter = request.GET.get('category')
    if category_filter:
        courses = Course.objects.filter(category__id=category_filter)
    else:
        courses = Course.objects.all()

    courses = courses.annotate(enrolled=Count(
        'enrollment')).order_by('-enrolled')
    categories = Category.objects.all()
    paginator = Paginator(courses, 8)  # 8 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses/course_list.html', {'courses': page_obj, 'categories': categories})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)
    user = request.user
    is_authenticated = user.is_authenticated

    # Default values for enrollment and completion status
    enrollment = None
    is_enrolled = False
    completed_lessons = []
    all_lessons_completed = False
    completion_rate = 0

    if is_authenticated:
        try:
            enrollment = Enrollment.objects.get(course=course, student=user)
            is_enrolled = True
            # Retrieve completed lessons
            completed_lessons = enrollment.completed_lessons.all()
            # Check if all lessons are completed
            all_lessons_completed = completed_lessons.count() == lessons.count()
            # Calculate completion rate
            completion_rate = (completed_lessons.count() / lessons.count()) * 100
        except Enrollment.DoesNotExist:
            pass

    context = {
        'course': course,
        'lessons': lessons,
        'is_authenticated': is_authenticated,
        'is_enrolled': is_enrolled,
        'completed_lessons': completed_lessons,
        'all_lessons_completed': all_lessons_completed,
        'enrollment': enrollment,
        'completion_rate': completion_rate,
    }

    return render(request, 'courses/course_detail.html', context)

# Enroll in a Course
@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if Enrollment.objects.filter(course=course, student=request.user).exists():
        messages.error(request, f'You are already enrolled in {course.title}.')
        return redirect('course_detail', course_id=course_id)

    Enrollment.objects.create(course=course, student=request.user)
    messages.success(
        request, f'You have successfully enrolled in {course.title}.')
    return redirect('course_detail', course_id=course_id)

# My Enrollments


@login_required
def my_enrollments(request):
    enrollments = Enrollment.objects.filter(student=request.user).order_by(
        '-enrolled_at').select_related('course')
    return render(request, 'courses/my_enrollments.html', {'enrollments': enrollments})

# Drop Course


@login_required
def drop_course(request, enrollment_id):
    enrollment = get_object_or_404(
        Enrollment, id=enrollment_id, student=request.user)
    enrollment.delete()
    messages.success(request, 'You have successfully dropped the course.')
    return redirect('my_enrollments')


@login_required
def lesson_detail(request, course_id, lesson_id):
    # Fetch the lesson and course details
    lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
    lessons = Lesson.objects.filter(course_id=course_id).order_by("order")
    course = get_object_or_404(Course, id=course_id)

    user = request.user

    # Check if the user is enrolled in the course
    try:
        enrollment = Enrollment.objects.get(course_id=course_id, student=user)
    except Enrollment.DoesNotExist:
        messages.error(request, "You are not enrolled in this course, please enroll.")
        return redirect('course_detail', course_id=course_id)

    # Find previous and next lessons based on their order
    prev_lesson = lessons.filter(order__lt=lesson.order).last()
    next_lesson = lessons.filter(order__gt=lesson.order).first()

    # Debugging: Print the prev/next lessons to ensure they exist
    print(f"Prev Lesson: {prev_lesson}")
    print(f"Next Lesson: {next_lesson}")

    # Mark lesson as complete
    if request.method == "POST" and "mark_complete" in request.POST:
        enrollment.completed_lessons.add(lesson)
        enrollment.save()
        return redirect("lesson_detail", course_id=course_id, lesson_id=lesson_id)

    context = {
        "lesson": lesson,
        "prev_lesson": prev_lesson,  
        "next_lesson": next_lesson, 
        "enrollment": enrollment,
        "lessons": lessons,
        "course": course,
    }
    return render(request, "courses/lesson_detail.html", context)


# Add Comment
@login_required
def add_comment(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(
                course=course, student=request.user, comment=comment_text)
            messages.success(request, 'Comment added successfully.')
        else:
            messages.error(request, 'Comment cannot be empty.')
        return redirect('course_detail', course_id=course_id)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Add Review


@login_required
def add_review(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        if rating and review_text:
            Review.objects.create(
                course=course, student=request.user, rating=rating, review=review_text)
            messages.success(request, 'Review added successfully.')
        else:
            messages.error(request, 'Both rating and review are required.')
        return redirect('course_detail', course_id=course_id)
    return JsonResponse({'error': 'Invalid request method'}, status=405)




# List Instructors
def instructor_list(request):
    instructors = CustomUser.objects.filter(is_instructor=True, is_active=True)
    return render(request, 'courses/instructor_list.html', {'instructors': instructors})

def instructor_detail(request, instructor_id):
    # Get the instructor object or return 404 if not found
    instructor = get_object_or_404(CustomUser, id=instructor_id)
    
    # Fetch all courses taught by this instructor
    courses = CourseInstructor.objects.filter(instructor=instructor).select_related('course')
    
    # Calculate enrollment statistics
    total_enrollments = Enrollment.objects.filter(course__in=courses.values_list('course', flat=True)).count()
    active_courses = courses.count()

    # Calculate highest and average enrollments
    enrollment_counts = Enrollment.objects.filter(course__in=courses.values_list('course', flat=True)).values('course').annotate(enrollment_count=Count('id'))
    highest_enrollment = enrollment_counts.order_by('-enrollment_count').first()
    average_enrollment = enrollment_counts.aggregate(average_enrollment=Count('id'))['average_enrollment']

    # Context data to pass to the template
    context = {
        "instructor": instructor,
        "courses": courses,
        "total_enrollments": total_enrollments,
        "active_courses": active_courses,
        "highest_enrollment": highest_enrollment,
        "average_enrollment": average_enrollment,
    }

    return render(request, 'courses/instructor_detail.html', context)


# Search Courses
def search_courses(request):
    query = request.GET.get('q', '')
    courses = Course.objects.filter(
        title__icontains=query) if query else Course.objects.none()
    return render(request, 'courses/search_results.html', {'courses': courses, 'query': query})

# Instructor Dashboard
@login_required
def instructor_dashboard(request):
    # Ensure the user is an instructor
    if not request.user.is_instructor:
        messages.error(request, 'You are not an instructor.')
        return redirect('index')
    
    instructor = request.user

    # Get all courses (if needed for the instructor to see all courses)
    courses = Course.objects.all()

    # Get the courses the instructor is associated with
    my_courses = CourseInstructor.objects.all().filter(instructor=instructor).select_related('course')

    return render(request, 'instructor/instructor_dashboard.html', {
        'instructor': instructor,
        'courses': courses,
        'my_courses': my_courses
    })

# Become an Instructor
@login_required
def become_instructor(request, course_id):
    if not request.user.is_instructor:
        messages.error(request, 'You are not an instructor.')
        return redirect('index')
    instructor = request.user
    course = get_object_or_404(Course, id=course_id)
    try:
        CourseInstructor.objects.create(course=course, instructor=instructor)
        messages.success(request, 'You are now an instructor for this course.')
    except IntegrityError:
        messages.error(request, 'You are already an instructor for this course.')
    return redirect('instructor_dashboard')

# Custom Error Views
def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_403(request, exception):
    return render(request, '403.html', status=403)


def error_500(request):
    return render(request, '500.html', status=500)


def error_400(request, exception):
    return render(request, '400.html', status=400)
