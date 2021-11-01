from django.shortcuts import render
from .models import Job
from faker import Faker

# Create your views here.
def name(request):
    return render(request, 'jobs/name.html')


def past_job(request):
    fake = Faker('ko_kr')
    name = request.POST.get('name')
    profile_image = request.FILES.get('profile_image')
    if not Job.objects.filter(name=name):  
        job = Job()
        job.name = name
        job.profile_image = profile_image
        job.past_job = fake.job()
        job.save()
    job = Job.objects.get(name=name)
    
    context = {'job': job}
    return render(request, 'jobs/past_job.html', context)
