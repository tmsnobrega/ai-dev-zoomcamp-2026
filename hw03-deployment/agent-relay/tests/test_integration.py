"""Exercise two agents through the running HTTP API, not internal functions."""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor

import httpx


def test_two_agents_deliver_one_task_exactly_once():
    base_url = os.environ["API_BASE_URL"].rstrip("/")
    enrollment_secret = os.environ["RELAY_ENROLLMENT_SECRET"]
    with httpx.Client(base_url=base_url, timeout=10) as client:
        sender_response = client.post(
            "/api/v1/agents",
            headers={"X-Enrollment-Secret": enrollment_secret},
            json={"name": "integration-sender"},
        )
        recipient_response = client.post(
            "/api/v1/agents",
            headers={"X-Enrollment-Secret": enrollment_secret},
            json={"name": "integration-recipient"},
        )
        assert sender_response.status_code == recipient_response.status_code == 201
        sender, recipient = sender_response.json(), recipient_response.json()
        sender_auth = {"Authorization": f"Bearer {sender['token']}"}
        recipient_auth = {"Authorization": f"Bearer {recipient['token']}"}

        sent = client.post(
            "/api/v1/tasks",
            headers=sender_auth,
            json={"to": recipient["agent_id"], "input": "hello PostgreSQL"},
        )
        assert sent.status_code == 201
        task_id = sent.json()["task_id"]

        def claim(worker_id: str) -> httpx.Response:
            return client.post(
                "/api/v1/tasks/claim",
                headers=recipient_auth,
                json={"worker_id": worker_id, "wait_seconds": 0},
            )

        with ThreadPoolExecutor(max_workers=2) as pool:
            responses = list(pool.map(claim, ("worker-one", "worker-two")))
        claimed = [response for response in responses if response.status_code == 200]
        assert len(claimed) == 1, [response.status_code for response in responses]
        assert sum(response.status_code == 204 for response in responses) == 1
        claim_data = claimed[0].json()
        assert claim_data["task_id"] == task_id

        completed = client.post(
            f"/api/v1/tasks/{task_id}/complete",
            headers=recipient_auth,
            json={"claim_token": claim_data["claim_token"], "output": "HELLO POSTGRESQL"},
        )
        assert completed.status_code == 200

        sender_view = client.get(f"/api/v1/tasks/{task_id}", headers=sender_auth)
        assert sender_view.status_code == 200
        assert sender_view.json()["status"] == "completed"
        assert sender_view.json()["output"] == "HELLO POSTGRESQL"
