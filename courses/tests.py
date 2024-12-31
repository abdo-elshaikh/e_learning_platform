from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Course, Enrollment

User = get_user_model()

class CoursesTest(TestCase):
    """Test the courses app."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        cls.instructor = User.objects.create_user(
            username='instructor',
            password='password-123',
            email='instructor@example.com',
            is_instructor=True
        )
        cls.student = User.objects.create_user(
            username='student',
            password='password-123',
            email='student@example.com',
            is_student=True
        )
        cls.category = Category.objects.create(
            name='Programming',
            description='Programming courses'
        )
        cls.course = Course.objects.create(
            title='Python Basics',
            description='Learn the basics of Python',
            price=19.99,
            rating=4.5,
            category=cls.category,
            instructor=cls.instructor
        )
        cls.enrollment = Enrollment.objects.create(
            student=cls.student,
            course=cls.course
        )

    def setUp(self):
        """Set up each test."""
        self.client.login(username='instructor', password='password-123')

    def test_category_model(self):
        """Test the Category model."""
        category = Category.objects.get(id=self.category.id)
        self.assertEqual(category.name, 'Programming')
        self.assertEqual(category.description, 'Programming courses')

    def test_course_model(self):
        """Test the Course model."""
        course = Course.objects.get(id=self.course.id)
        self.assertEqual(course.title, 'Python Basics')
        self.assertEqual(course.instructor, self.instructor)

    def test_enrollment_model(self):
        """Test the Enrollment model."""
        enrollment = Enrollment.objects.get(id=self.enrollment.id)
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.course, self.course)

    def test_course_list_view(self):
        """Test the course list view."""
        url = reverse('course_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_list.html')
        self.assertContains(response, 'Python Basics')

    def test_course_list_pagination(self):
        """Test course list pagination."""
        for i in range(15):
            Course.objects.create(
                title=f'Course {i}',
                description=f'Description {i}',
                price=10.99 + i,
                rating=4.0,
                category=self.category,
                instructor=self.instructor
            )
        url = reverse('course_list') + '?page=2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Course 10')

    def test_course_detail_view(self):
        """Test the course detail view."""
        url = reverse('course_detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_detail.html')
        self.assertContains(response, 'Python Basics')
        self.assertContains(response, '19.99')

    def test_enrollment_create_view(self):
        """Test enrollment creation."""
        self.client.login(username='student', password='password-123')
        url = reverse('enroll_in_course')
        data = {'student': self.student.id, 'course': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(user=self.student, course=self.course).exists())

    def test_invalid_enrollment_create(self):
        """Test invalid enrollment creation."""
        url = reverse('enroll_in_course')
        data = {'student': '', 'course': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_enrollment_delete_view(self):
        """Test enrollment deletion."""
        self.client.login(username='student', password='password-123')
        url = reverse('drop_course', args=[self.enrollment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Enrollment.objects.filter(id=self.enrollment.id).exists())

    def test_enrollment_delete_unauthorized(self):
        """Test unauthorized enrollment deletion."""
        another_user = User.objects.create_user(username='anotheruser', password='password-456')
        self.client.login(username='anotheruser', password='password-456')
        url = reverse('drop_course', args=[self.enrollment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)  # Assumes a 403 for unauthorized actions
        self.assertTrue(Enrollment.objects.filter(id=self.enrollment.id).exists())

    def test_protected_views_require_login(self):
        """Ensure protected views require login."""
        self.client.logout()
        url = reverse('my_enrollments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_my_enrollments_view(self):
        """Test enrollment list view."""
        url = reverse('my_enrollments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/my_enrollments.html')
        self.assertContains(response, 'Python Basics')
        self.assertContains(response, self.student.username)
