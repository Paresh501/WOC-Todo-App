from django.contrib import admin
from django.db import models
from .models import Task
from tinymce.widgets import TinyMCE

# Register your models here.

class TutorialAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Title/date", {'fields': ["task_title"]}),
        ("Content", {"fields": ["task_content"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }


admin.site.register(Task,TutorialAdmin)
