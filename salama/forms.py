from django import forms
from .models import Appointment, Patient
#login form.
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password'
    }))

#signup form
class SignupForm(forms.Form):
    username=forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
        }))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    password=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    confirm_password=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))


def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        


class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter New Password'
    }))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm New Password'
    }))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError("Passwords do not match")




    #form to register new patient.from
class RegisterPatientForm(forms.Form):
        first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter First Name'
        }))
        last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Last Name'
        }))
        id_number=forms.CharField(max_length=8, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter ID Number'
        }))
        phone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Phone Number'
        }))
        address = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter address'
        }))
        next_of_kin=forms.CharField(max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Next Of-Kin'
        }))

        def clean_id_number(self):
            id_number = self.cleaned_data.get('id_number')
            # Ensure ID number has exactly 11 digits
            if len(str(id_number)) != 8:
                raise forms.ValidationError("ID Number must be exactly 8 digits.")
            return id_number



class CheckReturningPatientForm(forms.Form):
    inpatient_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Inpatient Number'
    }))


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'appointment_date']

    # Optionally, you can add a list of patients in the form to make selection easier
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.all()  # Make sure this line is here
