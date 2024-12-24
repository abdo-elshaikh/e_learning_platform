from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
# validation imports
from django.core import validators, exceptions, checks, signing, mail


# Get the custom user model
CustomUser = get_user_model()

# Login Form


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Username',
                'autofocus': 'autofocus',
                'required': 'required',
                'autocomplete': 'username',
                'type': 'text'
            }),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Password',
                'required': 'required',
                'autocomplete': 'current-password',
                'type': 'password'
            }),
        label='Password'
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators = [
            validators.MaxLengthValidator(150)]
        self.fields['password'].validators = [validators.MinLengthValidator(3)]
        self.fields['username'].error_messages = {
            'required': 'This field is required'}
        self.fields['password'].error_messages = {
            'required': 'This field is required'}

    # data validation methods

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('User does not exist.')

        user = CustomUser.objects.get(username=username)
        if not user.check_password(password):
            raise forms.ValidationError('Invalid password.')

        return cleaned_data

# Registration Form


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Username',
                'type': 'text'
            }),
        label='Username'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Email (optional)',
                'type': 'email'
            }),
        label='Email',
        required=False,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Password',
                'type': 'password',
                'id': 'id_password1'
            }),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Confirm Password',
                'type': 'password',
                'id': 'id_password2'
            }),
        label='Confirm Password'
    )

    is_instructor = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'type': 'checkbox'
            }),
        label='Instructor',
        required=False
    )

    is_student = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'type': 'checkbox'
            }),
        label='Student',
        required=False
    )

    role = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Role',
                'type': 'text'
            }),
        label='Role',
        choices=[('instructor', 'Instructor'), ('student', 'Student')]
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators = [
            validators.MaxLengthValidator(150)]
        self.fields['password1'].validators = [
            validators.MinLengthValidator(3)]
        self.fields['password2'].validators = [
            validators.MinLengthValidator(3)]
        self.fields['username'].error_messages = {
            'required': 'This field is required'}
        self.fields['password1'].error_messages = {
            'required': 'This field is required'}
        self.fields['password2'].error_messages = {
            'required': 'This field is required'}

    # data validation methods
    def clean(self):
        cleaned_data = super().clean()
        print('cleaning data :', cleaned_data)
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        role = cleaned_data.get('role')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Passwords do not match')

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already in use.')

        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')

        if role == 'instructor':
            cleaned_data['is_instructor'] = True
            cleaned_data['is_student'] = False
        elif role == 'student':
            cleaned_data['is_instructor'] = False
            cleaned_data['is_student'] = True
        else:
            raise forms.ValidationError('Please select a role.')

        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1',
                  'password2', 'is_instructor', 'is_student']

# Password Reset Form


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )

    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators = [validators.EmailValidator()]
        self.fields['email'].error_messages = {
            'required': 'This field is required'}

    class Meta:
        model = CustomUser
        fields = ['email']

# Set Password Form


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label='Confirm New Password'
    )

    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].validators = [
            validators.MinLengthValidator(8)]
        self.fields['new_password2'].validators = [
            validators.MinLengthValidator(8)]
        self.fields['new_password1'].error_messages = {
            'required': 'This field is required'}
        self.fields['new_password2'].error_messages = {
            'required': 'This field is required'}

    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']

# Edit Profile Form


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators = [
            validators.MaxLengthValidator(150)]
        self.fields['email'].validators = [validators.EmailValidator()]
        self.fields['username'].error_messages = {
            'required': 'This field is required'}
        self.fields['email'].error_messages = {
            'required': 'This field is required'}

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('This username is already in use.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    class Meta:
        model = CustomUser
        fields = ['username', 'email']
