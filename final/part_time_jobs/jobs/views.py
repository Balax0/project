from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Job, Category, Application, Profile
from django.contrib.auth.models import User

# Home page with job listings and filtering
def home(request):
    jobs = Job.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    job_type = request.GET.get('job_type')

    if category_id:
        jobs = jobs.filter(category_id=category_id)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    return render(request, 'jobs/home.html', {'jobs': jobs, 'categories': categories})

# Job details page
def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_details.html', {'job': job})

# Posting a new job
def post_job(request):
    if request.method == 'POST':
        # Collect form data
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category_id = request.POST.get('category', '')
        location = request.POST.get('location', '').strip()
        job_type = request.POST.get('job_type', '').strip()
        pay_rate = request.POST.get('pay_rate', '').strip()

        # Validate required fields
        if not all([title, description, category_id, location, job_type, pay_rate]):
            messages.error(request, "All fields are required!")
            categories = Category.objects.all()
            return render(request, 'jobs/post_job.html', {'categories': categories})

        # Validate category
        category = get_object_or_404(Category, id=category_id)

        # Save the job to the database
        try:
            job = Job.objects.create(
                title=title,
                description=description,
                category=category,
                location=location,
                job_type=job_type,
                pay_rate=pay_rate,
            )
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    
    # If GET request or form validation fails
    categories = Category.objects.all()
    return render(request, 'jobs/post_job.html', {'categories': categories})

# Applying for a job
def apply_job(request, job_id):
    if request.method == 'POST':
        applicant_name = request.POST['applicant_name']
        resume = request.FILES['resume']
        job = get_object_or_404(Job, id=job_id)
        
        # Ensure that the user is logged in when applying for a job
        if request.user.is_authenticated:
            Application.objects.create(
                user=request.user,  # Associate the logged-in user with the application
                job=job,
                applicant_name=applicant_name,
                resume=resume
            )
            messages.success(request, "Application submitted successfully!")
            return redirect('home')
        else:
            messages.error(request, "You must be logged in to apply for a job.")
            return redirect('login')
    
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/apply_job.html', {'job': job})

# User login
def user_login(request):
    if request.method == 'POST':
        if 'register' in request.POST:  # Check if the user is registering
            username = request.POST['username']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('login')
            
            # Create a new user
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "User registered successfully. Please log in.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Error creating user: {e}")
        else:  # Existing user logs in
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('choose_role')  # Redirect to role selection page after login
            else:
                messages.error(request, 'Invalid username or password.')
                
    return render(request, 'jobs/login.html')

# Role selection after login
def choose_role(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated

    # Check if the user already has a profile assigned with a user type (seeker or poster)
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.user_type == 'seeker':
            return redirect('seeker_dashboard')  # Redirect to the seeker dashboard
        elif profile.user_type == 'poster':
            return redirect('poster_dashboard')  # Redirect to the poster dashboard
    except Profile.DoesNotExist:
        # Redirect to a role selection page where the user can choose seeker or poster
        return render(request, 'jobs/role.html')

# Seeker Dashboard (Displays job applications by the seeker)
def seeker_dashboard(request):
    # Get the applications made by the logged-in user
    applications = Application.objects.filter(user=request.user)
    
    # Get the jobs that the user has not applied for (suggested jobs)
    suggested_jobs = Job.objects.exclude(id__in=[app.job.id for app in applications])
    
    return render(request, 'jobs/seeker_dashboard.html', {
        'applications': applications,  # Jobs that the seeker has applied to
        'suggested_jobs': suggested_jobs  # Jobs that are suggested to the seeker
    })

def poster_dashboard(request):
    # Get the jobs posted by the logged-in user (poster)
    jobs = Job.objects.filter(user=request.user)
    
    return render(request, 'jobs/poster_dashboard.html', {
        'jobs': jobs  # Jobs that the poster has posted
    })

def user_logout(request):
    logout(request)  # This logs out the user
    return redirect('login')  # Redirect to the login page after logout