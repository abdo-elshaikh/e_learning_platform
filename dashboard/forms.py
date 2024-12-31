from django import forms
from courses.models import Course, Enrollment, Category
from users.models import CustomUser
from django.contrib import messages


# Course Form
class CourseForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        )
    )
    price = forms.DecimalField(
        label='Price',
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    category = forms.ModelChoiceField(
        label='Category',
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    instructor = forms.ModelChoiceField(
        label='Instructor',
        queryset=CustomUser.objects.filter(is_instructor=True),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    rating = forms.FloatField(
        label='Rating',
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Course
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        price = cleaned_data.get('price')
        category = cleaned_data.get('category')
        instructor = cleaned_data.get('instructor')
        rating = cleaned_data.get('rating')

        if not title or not description or not price or not category or not instructor or not rating:
            raise forms.ValidationError('All fields are required')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Select Category'
        self.fields['instructor'].empty_label = 'Select Instructor'

    def save(self, commit=True):
        course = super().save(commit=False)
        course.save()
        return course

    def __str__(self):
        return self.title


# Enrollment Form
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course', 'student']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].empty_label = 'Select Course'
        self.fields['student'].empty_label = 'Select Student'

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        student = cleaned_data.get('student')

        if not course or not student:
            raise forms.ValidationError('All fields are required')

        return cleaned_data

    def save(self, commit=True):
        enrollment = super().save(commit=False)
        enrollment.save()
        return enrollment

    def __str__(self):
        return f"{self.course.title} - {self.student.username}"

# Category Form

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Category Name'
        self.fields['description'].label = 'Category Description'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        if not name or not description:
            raise forms.ValidationError('All fields are required')

        return cleaned_data

    def save(self, commit=True):
        category = super().save(commit=False)
        category.save()
        return category

    def __str__(self):
        return self.name

# User Form


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'is_instructor',
                  'is_student', 'is_active', 'is_staff', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email'
        self.fields['is_instructor'].label = 'Instructor'
        self.fields['is_student'].label = 'Student'
        self.fields['is_active'].label = 'Active'
        self.fields['is_staff'].label = 'Staff'
        self.fields['is_superuser'].label = 'Superuser'

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        is_instructor = cleaned_data.get('is_instructor')
        is_student = cleaned_data.get('is_student')
        is_active = cleaned_data.get('is_active')
        is_staff = cleaned_data.get('is_staff')
        is_superuser = cleaned_data.get('is_superuser')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        return user

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
