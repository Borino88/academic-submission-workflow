import pytest
from fastapi.testclient import TestClient
from src.api import app
from src.models import Role, ManuscriptStatus

client = TestClient(app)

def test_health_check():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "HEALTHY"
    assert res.json()["active_manuscripts"] >= 1

def test_submit_manuscript():
    payload = {
        "title": "Quantum Error Correction in Topological Qubits",
        "abstract": "We present a numerical simulation of surface codes under correlated noise regimes with high fidelity.",
        "keywords": ["quantum computing", "error correction", "qubits"],
        "author_email": "author@quantum-lab.org"
    }
    res = client.post("/api/v1/manuscripts/submit", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUBMITTED"
    assert data["submission"]["title"] == payload["title"]
    return data["id"]

def test_editorial_workflow_and_peer_review():
    ms_id = test_submit_manuscript()
    
    # Author trying to assign editor should fail (403)
    res = client.post(
        f"/api/v1/manuscripts/{ms_id}/assign-editor?editor_email=lead@journal.org",
        headers={"X-Actor-Role": "AUTHOR"}
    )
    assert res.status_code == 403
    
    # Editor assigns editor
    res = client.post(
        f"/api/v1/manuscripts/{ms_id}/assign-editor?editor_email=lead@journal.org",
        headers={"X-Actor-Role": "EDITOR"}
    )
    assert res.status_code == 200
    assert res.json()["status"] == "UNDER_DESK_REVIEW"
    
    # Editor invites reviewer
    res = client.post(
        f"/api/v1/manuscripts/{ms_id}/invite-reviewer?reviewer_email=rev1@expert.edu",
        headers={"X-Actor-Role": "EDITOR"}
    )
    assert res.status_code == 200
    assert res.json()["status"] == "UNDER_PEER_REVIEW"
    
    # Reviewer submits scorecard
    scorecard = {
        "methodology_score": 5,
        "clarity_score": 4,
        "reproducibility_score": 5,
        "comments_for_author": "Excellent mathematical formulation and reproducible code.",
        "recommendation": "ACCEPT"
    }
    res = client.post(
        f"/api/v1/manuscripts/{ms_id}/reviews",
        json=scorecard,
        headers={"X-Actor-Role": "REVIEWER", "X-Actor-Email": "rev1@expert.edu"}
    )
    assert res.status_code == 200
    assert len(res.json()["reviews"]) == 1
    
    # Editor makes final acceptance decision
    decision = {
        "decision": "ACCEPTED",
        "rationale": "Unanimous reviewer approval and verified reproducibility manifest."
    }
    res = client.post(
        f"/api/v1/manuscripts/{ms_id}/decision",
        json=decision,
        headers={"X-Actor-Role": "EDITOR"}
    )
    assert res.status_code == 200
    assert res.json()["status"] == "ACCEPTED"
