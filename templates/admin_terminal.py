{% extends "base.html" %}
{% block content %}
<h2 class="mb-4"><i class="bi bi-terminal-fill"></i> Admin Terminal</h2>

<div class="card p-4 shadow-sm">
    <form method="post">
        {{ form.hidden_tag() }}
        {{ form.cmd(class="form-control") }}
        {{ form.submit(class="btn btn-warning mt-3 w-100") }}
    </form>
</div>

{% if output %}
<div class="card p-4 shadow-sm mt-4 bg-dark text-white">
    <h5>Output</h5>
    <pre>{{ output }}</pre>
</div>
{% endif %}
{% endblock %}
