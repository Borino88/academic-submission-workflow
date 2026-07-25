from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Header, Depends
from src.models import (
    ManuscriptSubmission, ManuscriptRecord, ReviewerScorecard,
    EditorialDecision, Role
)
from src.service import EditorialWorkflowService

app = FastAPI(
    title="Academic Submission Workflow Platform",
    description="Neutral open-source manuscript submission, desk-review, and peer-evaluation engine.",
    version="1.0.0"
)

workflow_service = EditorialWorkflowService()

def get_role_header(x_actor_role: Role = Header(default=Role.AUTHOR)) -> Role:
    return x_actor_role

def get_actor_email(x_actor_email: str = Header(default="guest@open-science.org")) -> str:
    return x_actor_email

@app.get("/health", tags=["System"])
def health_check() -> Dict[str, Any]:
    return {
        "status": "HEALTHY",
        "service": "academic-submission-workflow",
        "version": "1.0.0",
        "active_manuscripts": len(workflow_service.manuscripts)
    }

@app.post("/api/v1/manuscripts/submit", response_model=ManuscriptRecord, tags=["Author Portal"])
def submit_manuscript(submission: ManuscriptSubmission) -> ManuscriptRecord:
    return workflow_service.submit_manuscript(submission)

@app.get("/api/v1/manuscripts", response_model=List[ManuscriptRecord], tags=["Editorial Desk"])
def list_manuscripts() -> List[ManuscriptRecord]:
    return list(workflow_service.manuscripts.values())

@app.get("/api/v1/manuscripts/{ms_id}", response_model=ManuscriptRecord, tags=["Editorial Desk"])
def get_manuscript(ms_id: str) -> ManuscriptRecord:
    if ms_id not in workflow_service.manuscripts:
        raise HTTPException(status_code=404, detail="Manuscript not found")
    return workflow_service.manuscripts[ms_id]

@app.post("/api/v1/manuscripts/{ms_id}/assign-editor", response_model=ManuscriptRecord, tags=["Editorial Desk"])
def assign_editor(
    ms_id: str,
    editor_email: str,
    role: Role = Depends(get_role_header)
) -> ManuscriptRecord:
    try:
        return workflow_service.assign_editor(ms_id, editor_email, role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/v1/manuscripts/{ms_id}/invite-reviewer", response_model=ManuscriptRecord, tags=["Editorial Desk"])
def invite_reviewer(
    ms_id: str,
    reviewer_email: str,
    role: Role = Depends(get_role_header)
) -> ManuscriptRecord:
    try:
        return workflow_service.invite_reviewer(ms_id, reviewer_email, role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/v1/manuscripts/{ms_id}/reviews", response_model=ManuscriptRecord, tags=["Peer Review"])
def submit_review(
    ms_id: str,
    scorecard: ReviewerScorecard,
    role: Role = Depends(get_role_header),
    email: str = Depends(get_actor_email)
) -> ManuscriptRecord:
    try:
        return workflow_service.submit_review(ms_id, email, scorecard, role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/v1/manuscripts/{ms_id}/decision", response_model=ManuscriptRecord, tags=["Editorial Desk"])
def make_decision(
    ms_id: str,
    decision: EditorialDecision,
    role: Role = Depends(get_role_header)
) -> ManuscriptRecord:
    try:
        return workflow_service.make_decision(ms_id, decision, role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
