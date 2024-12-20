from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Admin, Patient,Appointment, Billing
from .forms import LoginForm,AppointmentForm
from .forms import BillingForm, SignupForm, PasswordResetForm, RegisterPatientForm, CheckReturningPatientForm
from random import randint
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            admin = Admin.objects.filter(username=username, password=password).first()
            if admin:
                request.session['admin_id'] = admin.id
                print("Session admin_id set to:", request.session['admin_id'])
                messages.success(request, 'Logged in successfully')

                return redirect('dashboard')  # Replace 'dashboard' with the actual URL name of your dashboard
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'admin_login.html', {'form': form})  # Ensure the template is in the right directory

def logout(request):
    request.session.flush()  # Clear session data
    return redirect('login')  # Redirect to login page after logout


def admin_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Create new admin
            admin = Admin(username=username, email=email, password=password)
            admin.save()
            messages.success(request, 'Sign up successful! You can now log in.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'admin_signup.html', {'form': form})



def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            try:
                admin = Admin.objects.get(username=username)
                admin.password = new_password
                admin.save()
                messages.success(request, 'Password reset successful! You can now log in with your new password.')
                return redirect('login')
            except Admin.DoesNotExist:
                messages.error(request, 'Invalid username')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})


#redirectin the admin after login

def dashboard(request):
    print('dashboard  accessed')
    admin_id = request.session.get('admin_id')
    try:
        admin = Admin.objects.get(id=admin_id)
        welcome_message = f"Welcome, {admin.username}."
        return render(request, 'admin_dashboard.html', {'welcome_message': welcome_message})
    except Admin.DoesNotExist:
        messages.error(request, "Admin session expired, please log in again.")
        return redirect('login')


#view to register patient and give ip no.


def register_patient(request):
    if request.method == 'POST':
        form = RegisterPatientForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            id_number=form.cleaned_data['id_number']
            next_of_kin=form.cleaned_data['next_of_kin']
            address = form.cleaned_data['address']

            # Generate unique inpatient number
            unique_number = f"{first_name[0].upper()}{last_name[0].upper()}{randint(100, 999)}"
            # Save patient data to the database
            patient = Patient(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                address=address,
                inpatient_number=unique_number,
                next_of_kin=next_of_kin,
                id_number=id_number,

            )
            patient.save()
            messages.success(request, f"Patient registered successfully! Inpatient Number: {unique_number}")
            return redirect('registerpatient')
    else:
        form = RegisterPatientForm()
    return render(request, 'register_patient.html', {'form': form})


#check exisiting patient.
def check_returning_patient(request):
    patient_details = None
    if request.method == 'POST':
        form = CheckReturningPatientForm(request.POST)
        if form.is_valid():
            inpatient_number = form.cleaned_data['inpatient_number']
            try:
                patient = Patient.objects.get(inpatient_number=inpatient_number)
                patient_details = patient
            except Patient.DoesNotExist:
                messages.error(request, "Patient not found!")
    else:
        form = CheckReturningPatientForm()
    return render(request, 'check_returning_patient.html', {'form': form, 'patient_details': patient_details})


#booking appointment.

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Fetch the patient object using the selected ID
            patient_id = form.cleaned_data['patient'].id  # Here we use the patient object, not just the ID
            try:
                patient = Patient.objects.get(id=patient_id)

                # Get the appointment date from the form
                appointment_date = form.cleaned_data['appointment_date']

                # Create a new appointment for the patient
                appointment = Appointment(patient=patient, appointment_date=appointment_date)
                appointment.save()

                # Success message
                messages.success(request, f"Appointment successfully booked for {patient.first_name} {patient.last_name}.")

                # Redirect to the same page (to show the updated list of appointments)
                return redirect('bookappointment')
            except Patient.DoesNotExist:
                    (messages.error(request, "Patient not found!"))
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AppointmentForm()

    # Fetch all booked appointments
    appointments = Appointment.objects.filter(status='booked')

    # Pass the form and appointments list to the template

    return render(request, 'book_appointment.html', {'form': form, 'appointments': appointments})


#about us page
def about(request):
    return render  (request , 'about us.html')
def departments(request):
    return render(request , 'department_detail.html')

def home(request):
    return render(request, 'home.html')

#billing view

def view_bills(request):
    bills=Billing.objects.all() # this will retrieve all bills
    return render (request ,'bills.html', {'bills':bills})

def pay_bill(request):
    bill =get_object_or_404(Billing, id=bill_id)
    if request.method =='POST':
        amount=float(request.POST.get('amount'))
        if amount > bill.balance_due():
            messages.error(request, 'payment exceeds the balance due')
        else:
            bill.amount_paid  += amount
            if bill.balance_due() < 0:
                bill.payment_status = 'Paid'
            bill.save()
            messages.success(request, f'Payment of {amount} made succesfully.')
    return render (request,'pay_bill.html', {'bill':bill})


#create bill
def create_bill(request):
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Billing record created successfully!')
            return redirect('views_bill')  # Redirect to the billing list
    else:
        form = BillingForm()
    return render(request, 'create_bill.html', {'form': form})