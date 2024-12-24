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

from users.models import CustomUser
from courses.models import Course, Category, Enrollment


faker = Faker()

# Seed superuser
CustomUser.objects.get_or_create(
    email="superuser@elearning",
    username="superuser",
    first_name="Super",
    last_name="User",
    is_staff=True,
    is_superuser=True,
)

# Seed regular users
for _ in range(10):
    CustomUser.objects.get_or_create(
        email=faker.email(),
        username=faker.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        is_staff=False,
    )

# Seed instructors
for _ in range(5):
    CustomUser.objects.get_or_create(
        email=faker.email(),
        username=faker.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        is_staff=True,
        is_instructor=True,
    )
    
# Seed students
for _ in range(10):
    CustomUser.objects.get_or_create(
        email=faker.email(),
        username=faker.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        is_staff=False,
        is_student=True,
    )


# Seed categories
categories = [
    {"name": "Development", "description": "Courses related to software development"},
    {"name": "Design", "description": "Courses related to graphic design"},
    {"name": "Marketing", "description": "Courses related to marketing strategies"},
    {"name": "Business", "description": "Courses related to business management"},
    {"name": "Finance", "description": "Courses related to financial management"},
    {"name": "Health", "description": "Courses related to health and wellness"},
    {"name": "Personal Development", "description": "Courses related to personal development"},
    {"name": "Photography", "description": "Courses related to photography"},
    {"name": "Music", "description": "Courses related to music production"},
    {"name": "Cooking", "description": "Courses related to cooking and culinary techniques"},
    {"name": "Language", "description": "Courses related to language learning"},
    {"name": "Art", "description": "Courses related to art and creativity"},
]
for category in categories:
    Category.objects.get_or_create(
        name=category["name"],
        description=category["description"],
    )

# Seed courses
categories = list(Category.objects.all())
instructors = list(CustomUser.objects.filter(is_instructor=True))

for _ in range(50):
    course = Course(
        title=faker.sentence(),
        description=faker.paragraph(),
        price=random.randint(10, 100),
        rating=random.uniform(0, 5),
        instructor=random.choice(instructors),
        category=random.choice(categories),
    )
    course.save()

# Seed enrollments
courses = list(Course.objects.all())
students = list(CustomUser.objects.filter(is_student=True))

for _ in range(100):
    enrollment = Enrollment(
        course=random.choice(courses),
        student=random.choice(students),
    )
    enrollment.save()
    

print("Demo data seeded successfully!")
