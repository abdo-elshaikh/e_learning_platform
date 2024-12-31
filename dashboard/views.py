from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course, Category, Enrollment
from users.models import CustomUser, Profile
from .forms import CourseForm, EnrollmentForm, CategoryForm, UserForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages


# dashboard home view and should be is superuser
@login_required
def dashboard_home(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to view this page')
        raise PermissionDenied()

    total_courses = Course.objects.count() if Course else 0
    total_users = CustomUser.objects.count() if CustomUser else 0
    total_enrollments = Enrollment.objects.count() if Enrollment else 0
    total_categories = Category.objects.count() if Category else 0

    context = {
        'total_courses': total_courses,
        'total_users': total_users,
        'total_enrollments': total_enrollments,
        'total_categories': total_categories
    }
    return render(request, 'dashboard/dashboard_home.html', context)


# List View for Courses
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'dashboard/course_list.html'
    context_object_name = 'courses'


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'dashboard/course_form.html'
    success_url = reverse_lazy('dashboard:course_list')

    def form_valid(self, form):
        messages.success(self.request, 'Course created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Course creation failed')
        return super().form_invalid(form)


# Update View for Courses
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'dashboard/course_form.html'
    success_url = reverse_lazy('dashboard:course_list')

    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Course update failed')
        return super().form_invalid(form)


# Delete View for Courses
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'dashboard/course_confirm_delete.html'
    success_url = reverse_lazy('dashboard:course_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Course deleted successfully')
        return super().delete(request, *args, **kwargs)


# List View for Users (CustomUser)
class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'dashboard/users_list.html'
    context_object_name = 'users'


# Create View for Users (CustomUser)
class UserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'dashboard/user_form.html'
    success_url = reverse_lazy('dashboard:users_list')

    def form_valid(self, form):
        messages.success(self.request, 'User created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'User creation failed')
        return super().form_invalid(form)


# Update View for Users (CustomUser)
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'dashboard/user_form.html'
    success_url = reverse_lazy('dashboard:users_list')

    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'User update failed')
        return super().form_invalid(form)


# Delete View for Users (CustomUser)
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'dashboard/user_confirm_delete.html'
    success_url = reverse_lazy('dashboard:users_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'User deleted successfully')
        return super().delete(request, *args, **kwargs)


# Detail View for Users (CustomUser)
class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'dashboard/user_detail.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = Enrollment.objects.filter(student=self.object)
        return context


# List View for Enrollments
class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'dashboard/enrollment_list.html'
    context_object_name = 'enrollments'


# Create View for Enrollments
class EnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'dashboard/enrollment_form.html'
    success_url = reverse_lazy('dashboard:enrollment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Enrollment created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Enrollment creation failed')
        return super().form_invalid(form)


# Update View for Enrollments
class EnrollmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'dashboard/enrollment_form.html'
    success_url = reverse_lazy('dashboard:enrollment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Enrollment updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Enrollment update failed')
        return super().form_invalid(form)


# Delete View for Enrollments
class EnrollmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Enrollment
    template_name = 'dashboard/enrollment_confirm_delete.html'
    success_url = reverse_lazy('dashboard:enrollment_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Enrollment deleted successfully')
        return super().delete(request, *args, **kwargs)


# Category List View
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/category_list.html'
    context_object_name = 'categories'

# Category Create View
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard:category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Category creation failed')
        return super().form_invalid(form)

# Category Update View


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard:category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Category update failed')
        return super().form_invalid(form)

# Category Delete View


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'dashboard/category_confirm_delete.html'
    success_url = reverse_lazy('dashboard:category_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted successfully')
        return super().delete(request, *args, **kwargs)


# instructor list view
class InstructorListView(LoginRequiredMixin, ListView):
    model = CustomUser
    form_class = UserForm
    template_name = 'dashboard/instructor_list.html'
    context_object_name = 'instructors'
    queryset = CustomUser.objects.filter(is_instructor=True)

# student list view


class StudentListView(LoginRequiredMixin, ListView):
    model = CustomUser
    form_class = UserForm
    template_name = 'dashboard/student_list.html'
    context_object_name = 'students'
    queryset = CustomUser.objects.filter(is_student=True)
