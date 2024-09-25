from django import forms
from todo.models import Task, Tag

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["content", "deadline", "is_done", "tags"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
