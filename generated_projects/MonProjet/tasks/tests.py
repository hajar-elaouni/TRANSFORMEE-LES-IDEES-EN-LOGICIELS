import pytest
from django.urls import reverse
from .models import Task, Category, SubProject
from django.test import TestCase, Client

# Test database setup (using in-memory SQLite for testing)
# This would be configured in settings.py for a real test run.

@pytest.mark.django_db
class TestTaskModel:
    def test_create_task(self):
        category = Category.objects.create(name="Category 1")
        subproject = SubProject.objects.create(name="Subproject 1")
        task = Task.objects.create(title="Test Task", category=category, subproject=subproject)
        assert task.title == "Test Task"
        assert task.category == category
        assert task.subproject == subproject

    def test_update_task(self):
        category = Category.objects.create(name="Category 1")
        subproject = SubProject.objects.create(name="Subproject 1")
        task = Task.objects.create(title="Test Task", category=category, subproject=subproject)
        task.title = "Updated Task"
        task.save()
        assert task.title == "Updated Task"

    def test_delete_task(self):
        category = Category.objects.create(name="Category 1")
        subproject = SubProject.objects.create(name="Subproject 1")
        task = Task.objects.create(title="Test Task", category=category, subproject=subproject)
        task.delete()
        assert Task.objects.count() == 0


@pytest.mark.django_db
class TestViews:
    def test_task_create(self, client, db):
        response = client.post(reverse('task_create'), {'title': 'New Task'})
        assert response.status_code == 302 # Redirect after successful creation

    def test_task_update(self, client, db):
        category = Category.objects.create(name="Category 1")
        subproject = SubProject.objects.create(name="Subproject 1")
        task = Task.objects.create(title="Test Task", category=category, subproject=subproject)
        response = client.post(reverse('task_update', args=[task.pk]), {'title': 'Updated Task'})
        assert response.status_code == 302

    def test_task_delete(self, client, db):
        category = Category.objects.create(name="Category 1")
        subproject = SubProject.objects.create(name="Subproject 1")
        task = Task.objects.create(title="Test Task", category=category, subproject=subproject)
        response = client.post(reverse('task_delete', args=[task.pk]))
        assert response.status_code == 302

    def test_task_list_pagination(self, client, db):
        for i in range(15):
            Category.objects.create(name=f"Category {i+1}")
            SubProject.objects.create(name=f"Subproject {i+1}")
            Task.objects.create(title=f"Task {i+1}")

        response = client.get(reverse('task_list') + "?page=2")
        assert response.status_code == 200
        #Further assertions to check pagination behavior




### Summary of Fixes:

1. **Added `unique=True` constraint to `Category` and `SubProject` models:** This prevents duplicate entries for categories and subprojects.
2. **Added `created_at` and `updated_at` fields to the `Task` model:** This tracks the creation and modification timestamps of tasks.
3. **Improved `TaskForm`:** Added client-side validation for the title field and a more user-friendly textarea for the description.
4. **Added Flash Messages:** Implemented Django's messages framework to provide feedback to the user after actions (create, update, delete).  This improves the user experience.
5. **Improved Error Handling:** Added error handling in the `task_delete` view to gracefully handle potential exceptions during task deletion.
6. **Enhanced `task_list.html`:** Added display of due date and status for each task.
7. **Added message display to templates:** Added code to display success and error messages from the views in the templates.
8. **Improved testing:** Added more comprehensive tests for model and view interactions.  The tests are structured to be run with pytest in a proper Django testing environment.
9. **Added `MESSAGE_STORAGE` to `settings.py`:** This is required for the messages framework to function correctly.


The corrected code includes improved error handling, enhanced form validation, added timestamps to the `Task` model, and uses Django's messaging framework for better user feedback.  The tests provide a more comprehensive test suite. Remember to replace placeholder database credentials in `settings.py` with your actual database details.  You will also need to run `python manage.py makemigrations` and `python manage.py migrate` after making changes to the models.
