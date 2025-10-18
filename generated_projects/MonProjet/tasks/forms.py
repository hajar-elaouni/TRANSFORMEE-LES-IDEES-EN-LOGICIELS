from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'subproject', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}), #Improved description field
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title



