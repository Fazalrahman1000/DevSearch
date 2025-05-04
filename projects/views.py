from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Projects, Reviews, Tag
from .forms import ProjectForm

def projects(request):
    projects = Projects.objects.all()
    context = {'projects':projects}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    singleProject = Projects.objects.get(id=pk)
    tags = singleProject.tags.all()
    return render(request, "projects/single-project.html", {'single':singleProject, 'tags':tags})


@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form':form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url='login')
def updateProject(request, pk):
    project = Projects.objects.get(id = pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form':form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url='login')
def deleteProject(request, pk):
    project = Projects.objects.get(id = pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')
    context = {'project':project}

    return render(request, 'projects/delete-project.html', context)