from .views import index, course_detail, category_list, category_detail, course_list, enroll_in_course, my_enrollments, drop_course, error_404, error_500, error_403, error_400
from django.urls import path
from django.conf.urls import handler404, handler403, handler500, handler400

handler404 = error_404
handler403 = error_403
handler500 = error_500
handler400 = error_400

urlpatterns = [
    path('', index, name='index'),
    path('categories/', category_list, name='category_list'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
    path('courses/', course_list, name='course_list'),
    path('courses/<int:course_id>/', course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', enroll_in_course, name='enroll_in_course'),
    path('my-enrollments/', my_enrollments, name='my_enrollments'),
    path('drop/<int:enrollment_id>/', drop_course, name='drop_course'),
]
