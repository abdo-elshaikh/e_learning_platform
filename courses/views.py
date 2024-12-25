from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Course, Enrollment
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.db.models import Count
from django.contrib import messages


# Create your views here.

from django.db.models import Count, F


def index(request):
    # Fetch categories and order them before applying the slice
    categories = Category.objects.all().order_by('-created_at')
    categories = categories[:4]
    # Fetch courses and order them by enrollments before applying the slice
    courses = Course.objects.annotate(
        enrolled=Count('enrollment')).order_by('-enrolled')
    courses = courses[:4]  # Apply slice after ordering

    # Round the rating to 2 decimal places
    for course in courses:
        course.rating = round(course.rating, 2)

    total_courses = Course.objects.count()
    total_categories = Category.objects.count()

    return render(request, 'courses/home.html', {
        'categories': categories,
        'courses': courses,
        'total_courses': total_courses,
        'total_categories': total_categories,
    })

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
    if request.GET.get('category'):
        courses = Course.objects.filter(
            category__id=request.GET.get('category'))
    else:
        courses = Course.objects.all()

    courses = courses.annotate(enrolled=Count(
        'enrollment')).order_by('-enrolled')
    categories = Category.objects.all()
    # Pagination setup
    page = int(request.GET.get('page', 1))
    paginator = Paginator(courses, 8)
    page_obj = paginator.get_page(page)

    return render(request, 'courses/course_list.html', {'courses': page_obj, 'categories': categories})

# Course Detail


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

# Enroll in a Course


@login_required
def enroll_in_course(request, course_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to enroll in a course.')
        return redirect('course_list')
    course = get_object_or_404(Course, id=course_id)
    if Enrollment.objects.filter(course=course, student=request.user).exists():
        messages.error(request, f'You are already enrolled in {course.title}')
        return redirect('course_list')

    Enrollment.objects.create(course=course, student=request.user)
    messages.success(request, f'You have successfully enrolled in {course.title}')
    return redirect('course_list')

# My Enrollments
@login_required
def my_enrollments(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to view your enrollments.')
        return redirect('index')
    enrollments = Enrollment.objects.filter(student=request.user).order_by(
        '-enrolled_at').select_related('course')
    return render(request, 'courses/my_enrollments.html', {'enrollments': enrollments})

# Drop Course


@login_required
def drop_course(request, enrollment_id):
    enrollment = get_object_or_404(
        Enrollment, id=enrollment_id, student=request.user)
    if not enrollment:
        return JsonResponse({'message': 'Enrollment not found.'}, status=404)
    enrollment.delete()
    return redirect('my_enrollments')

# define custom error views


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_403(request, exception):
    return render(request, '403.html', status=403)


def error_500(request, exception):
    return render(request, '500.html', status=500)


def error_400(request, exception):
    return render(request, '400.html', status=400)
