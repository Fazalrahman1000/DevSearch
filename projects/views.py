from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
projectslist = [
        {
            'id':'1',
            'name':'Ecommerce website',
            'description':'one of good website for business'
        },
        {
            'id':'2',
            'name':'Education website',
            'description':'one of good website for education'
        },
        {
            'id':'3',
            'name':'Exam website',
            'description':'one of good website for examinations'
        },
    ]

def projects(request):
    context = {'projects':projectslist}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    singleProject = None
    for project in projectslist:
        if project['id'] == pk:
            singleProject = project
    return render(request, "projects/single-project.html", {'single':singleProject})