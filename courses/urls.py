from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # about page
    path('about/', views.about, name='about'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),

    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),

    # Enrollments
    path('courses/<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('my-enrollments/', views.my_enrollments, name='my_enrollments'),
    path('enrollments/<int:enrollment_id>/drop/', views.drop_course, name='drop_course'),

    # Lessons
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),

    # Comments
    path('courses/<int:course_id>/comments/add/', views.add_comment, name='add_comment'),

    # Reviews
    path('courses/<int:course_id>/reviews/add/', views.add_review, name='add_review'),
    # become instructor
    path('courses/<int:course_id>/become-instructor/', views.become_instructor, name='become_instructor'),

    # Instructors
    path('instructors/', views.instructor_list, name='instructor_list'),
    path('instructors/<int:instructor_id>/', views.instructor_detail, name='instructor_detail'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),

    # Search
    path('search/', views.search_courses, name='search_courses'),
]

# Custom error handlers
handler404 = 'courses.views.error_404'
handler403 = 'courses.views.error_403'
handler500 = 'courses.views.error_500'
handler400 = 'courses.views.error_400'
