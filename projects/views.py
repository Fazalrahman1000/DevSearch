from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Projects, Reviews, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, paginateProjects

def projects(request):

    projects, search_query = search_projects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects':projects, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    singleProject = Projects.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = singleProject
        review.owner = request.user.profile
        review.save()

        singleProject.getVoteCount

        messages.success(request, 'Review Added successfully')
        return redirect('project',pk = singleProject.id)
    
    tags = singleProject.tags.all()
    return render(request, "projects/single-project.html", {'single':singleProject, 'tags':tags, 'form':form})


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project =  form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form':form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id = pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id = pk)
    if request.method == "POST":
        project.delete()
        messages.success(request,'Project Deleted Successfully!')
        return redirect('account')
    context = {'project':project}

    return render(request, 'delete-template.html', context)