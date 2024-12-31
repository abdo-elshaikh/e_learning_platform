from django.contrib import admin

# Register your models here.
from .models import Course, Enrollment, Category, Comment, Lesson, CourseInstructor, Review

admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Category)
admin.site.register(CourseInstructor)
admin.site.register(Comment)
admin.site.register(Lesson)
admin.site.register(Review)
