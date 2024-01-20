from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobSerializer, ApplyJobSerializer, ResumeSerializer
from .form import CreateJobForm
from job.models import Job, ApplyJob
from resume.models import Resume

@api_view(['GET'])
def job_details_api(request, pk):
    try:
        job = Job.objects.get(pk=pk)
        related_jobs = Job.objects.filter(company=job.company).exclude(pk=pk)[:3]
        
        job_serializer = JobSerializer(job)
        related_jobs_serializer = JobSerializer(related_jobs, many=True)
        
        response_data = {
            'job': job_serializer.data,
            'related_jobs': related_jobs_serializer.data
        }
        return Response(response_data, status=200)
    except Job.DoesNotExist:
        response_data = {'message': 'Job not found.'}
        return Response(response_data, status=404)
    

@api_view(['POST'])
def create_job_api(request):
    if request.user.is_recruiter and request.user.has_company:
        form = CreateJobForm(request.data)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.company = request.user.company
            job.save()
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        response_data = {'message': 'Permission denied.'}
        return Response(response_data, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
def company_jobs_api(request, pk):
    try:
        jobs = Job.objects.filter(company_id=pk)
        job_serializer = JobSerializer(jobs, many=True)
        return Response(job_serializer.data, status=200)
    except Job.DoesNotExist:
        response_data = {'message': 'Company jobs not found.'}
        return Response(response_data, status=404)
    
@api_view(['GET'])
def job_resumes_api(request, pk):
    try:
        job = Job.objects.get(pk=pk)

        job_serializer = JobSerializer(job)
        resumes = Resume.objects.filter(job=job)
        resumes_serializer = ResumeSerializer(resumes, many=True)

        response_data = {
            'job': job_serializer.data,
            'resumes': resumes_serializer.data
        }
        return Response(response_data, status=200)
    except Job.DoesNotExist:
        response_data = {'message': 'Job not found.'}
        return Response(response_data, status=404)
    
@api_view(['GET'])
def specific_resume_api(request, job_id, user_id):
    try:
        resume = Resume.objects.get(user_id=user_id)
        apply_job = ApplyJob.objects.get(job_id=job_id, resume=resume)
        
        resume_serializer = ResumeSerializer(resume)
        job_serializer = JobSerializer(apply_job.job)
        
        response_data = {
            'job': job_serializer.data,
            'resume': resume_serializer.data
        }
        return Response(response_data, status=200)
    except (Resume.DoesNotExist, ApplyJob.DoesNotExist):
        response_data = {'message': 'Resume not found for the specified job.'}
        return Response(response_data, status=404)