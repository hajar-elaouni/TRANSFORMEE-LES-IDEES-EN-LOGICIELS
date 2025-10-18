<h1>Delete Task</h1>
<p>Are you sure you want to delete "{{ task.title }}"?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit">Yes</button>
    <a href="{% url 'task_list' %}">No</a>
</form>




# settings.py (Add to INSTALLED_APPS and DATABASES)

INSTALLED_APPS = [
    # ... other apps
    'tasks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'your_database_host',
        'PORT': 'your_database_port',
    }
}

# Add this to settings.py for messages framework
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'



