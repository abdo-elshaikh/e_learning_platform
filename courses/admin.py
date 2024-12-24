from django.contrib import admin

# Register your models here.
from .models import Course, Enrollment, Category

admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Category)
