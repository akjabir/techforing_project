from django.contrib import admin
from foring.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(Task)
admin.site.register(Comment)
