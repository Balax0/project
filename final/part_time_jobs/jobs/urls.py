from django.urls import path
from . import views

urlpatterns = [
    # Set login page as home page
    path('', views.user_login, name='login'),  # Login as the home page

    # Home page for logged-in users
    path('home/', views.home, name='home'),  # Redirect to home after login

    # Job-related URLs
    path('job/<int:job_id>/', views.job_details, name='job_details'),
    path('post-job/', views.post_job, name='post_job'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),

    # Dashboard URLs (for seekers and posters)
    path('dashboard/seeker/', views.seeker_dashboard, name='seeker_dashboard'),
    path('dashboard/poster/', views.poster_dashboard, name='poster_dashboard'),

     # Role selection URL
    path('choose-role/', views.choose_role, name='choose_role'),
    path('logout/', views.user_logout, name='logout'),

]
