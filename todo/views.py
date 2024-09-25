from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from todo.models import Task, Tag
from todo.forms import TaskForm, TagForm


class TaskListView(ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = 'tasks'
    ordering = ["is_done", "-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("todo:task-list")


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("todo:task-list")


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("todo:task-list")


class TagListView(ListView):
    model = Tag
    template_name = "tag_list.html"
    context_object_name = "tags"


class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tag_form.html"
    success_url = reverse_lazy("todo:tag-list")


class TagUpdateView(UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "tag_form.html"
    success_url = reverse_lazy("todo:tag-list")


class TagDeleteView(DeleteView):
    model = Tag
    template_name = "tag_confirm_delete.html"
    success_url = reverse_lazy("todo:tag-list")


def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_done = not task.is_done
    task.save()
    return redirect("todo:task-list")
