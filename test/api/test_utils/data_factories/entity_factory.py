import allure
from datetime import datetime, timedelta, timezone


def create_task(auth_client, **kwargs):
    """Helper to create a task with custom properties"""
    payload = {
        "title": kwargs.get("title", "Sample Task"),
        "description": kwargs.get("description", ""),
        "status": kwargs.get("status", "open"),
    }

    with allure.step(f"Create task: {payload['title']}"):
        response = auth_client.post('/api/tasks', data=payload)
        assert response.status_code == 201, f"Failed to create task: {response.text}"
        task = response.json

    return task


def create_project(auth_client, **kwargs):
    """Helper to create a project with custom properties"""
    payload = {
        "title": kwargs.get("title", "Test Project"),
        "description": kwargs.get("description", ""),
        "win_condition": kwargs.get("win_condition", ""),
        "reason": kwargs.get("reason", ""),
        "next_step": kwargs.get("next_step", ""),
    }

    with allure.step(f"Create project: {payload['title']}"):
        response = auth_client.post('/api/projects', data=payload)
        assert response.status_code == 201, f"Failed to create project: {response.text}"
        project = response.json

    return project


