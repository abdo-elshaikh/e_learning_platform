from django.urls import path
from .views import (
    dashboard_home,
    CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
    EnrollmentListView, EnrollmentCreateView, EnrollmentUpdateView, EnrollmentDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    InstructorListView, StudentListView, UserDetailView,
    LessonListView, LessonCreateView, LessonUpdateView, LessonDeleteView, LessonDetailView
)

app_name = 'dashboard'

urlpatterns = [
    
    # Dashboard Home
    path('', dashboard_home, name='dashboard_home'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/',
         CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/',
         CategoryDeleteView.as_view(), name='category_delete'),

    # Course URLs
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/create/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    
    # Lesson URLs
    path('lessons/', LessonListView.as_view(), name='lesson_list'),
    path('lessons/add/', LessonCreateView.as_view(), name='lesson_add'),
    path('lessons/<int:pk>/edit/', LessonUpdateView.as_view(), name='lesson_edit'),
    path('lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),

    # User URLs
    path('users/', UserListView.as_view(), name='users_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

    # Instructor URLs
    path('instructors/', InstructorListView.as_view(), name='instructor_list'),
    path('students/', StudentListView.as_view(), name='student_list'),

    # Enrollment URLs
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/create/', EnrollmentCreateView.as_view(),
         name='enrollment_create'),
    path('enrollments/<int:pk>/edit/',
         EnrollmentUpdateView.as_view(), name='enrollment_edit'),
    path('enrollments/<int:pk>/delete/',
         EnrollmentDeleteView.as_view(), name='enrollment_delete'),
]
