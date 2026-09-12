from fastapi.testclient import TestClient

from app.main import create_app


def test_task_lifecycle_and_persistence(tmp_path):
    url = f"sqlite:///{tmp_path / 'tasks.sqlite3'}"
    with TestClient(create_app(url)) as client:
        assert client.get("/api/tasks").json() == []
        created = client.post("/api/tasks", json={"title": "  Write report  ", "description": "Draft"})
        assert created.status_code == 201
        task = created.json()
        assert task["title"] == "Write report"
        assert task["status"] == "todo"
        moved = client.patch(f"/api/tasks/{task['id']}", json={"status": "doing"})
        assert moved.status_code == 200
        assert moved.json()["status"] == "doing"

    with TestClient(create_app(url)) as client:
        assert len(client.get("/api/tasks").json()) == 1
        assert client.delete(f"/api/tasks/{task['id']}").status_code == 204
        assert client.get("/api/tasks").json() == []


def test_invalid_input_and_missing_task_do_not_change_data(tmp_path):
    with TestClient(create_app(f"sqlite:///{tmp_path / 'tasks.sqlite3'}")) as client:
        assert client.post("/api/tasks", json={"title": "   "}).status_code == 422
        assert client.post("/api/tasks", json={"title": "x" * 101}).status_code == 422
        assert client.patch("/api/tasks/1", json={"status": "blocked"}).status_code == 422
        assert client.patch("/api/tasks/1", json={"status": "done"}).status_code == 404
        assert client.delete("/api/tasks/1").status_code == 404
        assert client.get("/api/tasks").json() == []

