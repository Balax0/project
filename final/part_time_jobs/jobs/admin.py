#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'job_type', 'pay_rate', 'posted_at')
    search_fields = ('title', 'category__name', 'location')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'job', 'applied_at')
    search_fields = ('applicant_name', 'job__title')
