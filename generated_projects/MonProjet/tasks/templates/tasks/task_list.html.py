<h1>Task List</h1>
{% if messages %}
    <ul class="messages">
        {% for message in messages %}
            <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
        {% endfor %}
    </ul>
{% endif %}
{% if tasks.has_other_pages %}
    <ul class="pagination">
        {% if tasks.has_previous %}
            <li><a href="?page={{ tasks.previous_page_number }}">&laquo;</a></li>
        {% endif %}
        {% for i in tasks.paginator.page_range %}
            {% if tasks.number == i %}
                <li class="active"><a href="#">{{ i }}</a></li>
            {% else %}
                <li><a href="?page={{ i }}">{{ i }}</a></li>
            {% endif %}
        {% endfor %}
        {% if tasks.has_next %}
            <li><a href="?page={{ tasks.next_page_number }}">&raquo;</a></li>
        {% endif %}
    </ul>
{% endif %}
<ul>
    {% for task in tasks %}
        <li>
            <a href="{% url 'task_update' task.pk %}">{{ task.title }}</a> -
            <a href="{% url 'task_delete' task.pk %}">Delete</a>
            <span>Due: {{ task.due_date }}</span> <span>Status: {{ task.get_status_display }}</span>
        </li>
    {% endfor %}
</ul>
<a href="{% url 'task_create' %}">Create New Task</a>



