from django.db import models
from django.contrib.auth.models import User


# Category model for categorizing jobs
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Job model representing job postings
class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50, choices=[('Part-time', 'Part-time'), ('Gig', 'Gig')])
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2)
    posted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')  # Added user field

    def __str__(self):
        return self.title


# Application model representing job applications by seekers
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Associated with a user (applicant)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant_name} - {self.job.title}"


# Profile model for distinguishing job seekers and posters
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('seeker', 'Job Seeker'),
        ('poster', 'Job Poster'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
