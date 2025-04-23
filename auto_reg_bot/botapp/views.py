from django.shortcuts import render, redirect
from .forms import BotJobForm
from .bot import run_bot
from django.shortcuts import render

def create_account_job(request):
    if request.method == 'POST':
        form = BotJobForm(request.POST)
        if form.is_valid():
            job = form.save()
            run_bot(job)  # call the bot script
            return redirect('job-success')
    else:
        form = BotJobForm()
    return render(request, 'botapp/create_accounts.html', {'form': form})


def job_success(request):
    return render(request, 'botapp/job_success.html', {'message': 'Job created successfully!'})