from django.test import TestCase
from django.urls import reverse

from todo.models import Tag, Task


class TagModelTest(TestCase):
    def test_str(self) -> None:
        tag = Tag.objects.create(name="Work")
        self.assertEqual(str(tag), tag.name)

class TaskModelTest(TestCase):
    def test_str(self) -> None:
        task = Task.objects.create(content="Finish project")
        self.assertEqual(str(task), task.content)


class TaskListViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(content="Test task")
        self.url = reverse("todo:task-list")

    def test_task_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test task")


class TaskDeleteViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(content="Delete this task")
        self.url = reverse("todo:task-delete", kwargs={"pk": self.task.pk})

    def test_delete_task(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("todo:task-list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

class TaskCreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse("todo:task-add")
        self.tag = Tag.objects.create(name="Important")

    def test_create_task(self):
        response = self.client.post(self.url, {
            "content": "New task",
            "deadline": "2024-09-25T12:00",
            "is_done": False,
            "tags": [self.tag.pk]
        })
        self.assertRedirects(response, reverse("todo:task-list"))
        self.assertTrue(Task.objects.filter(content="New task").exists())

class TaskUpdateViewTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Important")
        self.task = Task.objects.create(content="Old task", deadline="2024-09-25T12:00", is_done=False)
        self.task.tags.add(self.tag)
        self.url = reverse("todo:task-update", kwargs={"pk": self.task.pk})

    def test_update_task(self):
        response = self.client.post(self.url, {
            "content": "Updated task",
            "deadline": "2024-09-26T12:00",
            "is_done": True,
            "tags": [self.tag.pk]
        })
        self.assertRedirects(response, reverse("todo:task-list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.content, "Updated task")
        self.assertEqual(self.task.is_done, True)

class ToggleTaskStatusTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(content="Toggle task")

    def test_toggle_status(self):
        url = reverse("todo:task-toggle", kwargs={"pk": self.task.pk})
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_done)
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_done)
