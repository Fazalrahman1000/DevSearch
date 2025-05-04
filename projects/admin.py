from django.contrib import admin
from .models import Projects, Reviews, Tag
# Register your models here.

admin.site.register(Projects)
admin.site.register(Reviews)
admin.site.register(Tag)