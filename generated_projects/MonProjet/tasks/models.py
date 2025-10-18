from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True) # Added unique constraint

    def __str__(self):
        return self.name

class SubProject(models.Model):
    name = models.CharField(max_length=100, unique=True) # Added unique constraint

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = (
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low'),
    )
    STATUS_CHOICES = (
        ('todo', 'À faire'),
        ('inprogress', 'En cours'),
        ('done', 'Terminé'),
        ('blocked', 'Bloquée'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    subproject = models.ForeignKey(SubProject, on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # Added created timestamp
    updated_at = models.DateTimeField(auto_now=True)     # Added updated timestamp

    def __str__(self):
        return self.title



