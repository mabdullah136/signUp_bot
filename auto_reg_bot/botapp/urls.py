from django.urls import path
from .views import create_account_job, job_success

urlpatterns = [
    path('create/', create_account_job, name='create-job'),
    path('success/', job_success, name='job-success'),
]