from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
# validation imports
from django.core import validators, exceptions, checks, signing, mail
from django.contrib.auth import authenticate


# Get the custom user model
CustomUser = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Username',
            }
        ),
        label='Username',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Password',
            }
        ),
        label='Password',
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username or not password:
            raise forms.ValidationError(
                "Both username and password are required.")

        # Retrieve the user to check if it exists and is active
        try:
            User = get_user_model()
            user = User.objects.get(username=username)
            if not user.is_active:
                raise forms.ValidationError(
                    "This account is inactive. Please contact the admin.")
        except User.DoesNotExist:
            raise forms.ValidationError(
                "Invalid username or password, or account does not exist.")

        # Authenticate the user after verifying the account's existence and status
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid username or password.")

        self.user_cache = user
        return self.cleaned_data

# Registration Form


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Username',
            }),
        label='Username'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Email (optional)',
            }),
        label='Email',
        required=False
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Password',
            }),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Confirm Password',
            }),
        label='Confirm Password'
    )
    role = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-radio mt-1 block'
            }),
        label='Role',
        choices=[('instructor', 'Instructor'), ('student', 'Student')],
        initial='student'
    )

    def clean(self):
        cleaned_data = super().clean()
        print('cleaned_data: ', cleaned_data)
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        role = cleaned_data.get('role')

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        if username == password1:
            raise forms.ValidationError(
                'Password should not be the same as username.')
        if not role:
            raise forms.ValidationError('Role is required.')
        return cleaned_data

    def save(self, commit=True, role=None):
        if role is None:
            raise ValueError('Role is required.')
        else:
            if role == 'instructor':
                self.instance.is_instructor = True
                self.instance.is_student = False
                self.instance.is_active = False
            else:
                self.instance.is_student = True
                self.instance.is_instructor = False
                self.instance.is_active = True
        return super().save(commit=commit)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

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
