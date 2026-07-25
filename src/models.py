from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class Role(str, Enum):
    AUTHOR = "AUTHOR"
    EDITOR = "EDITOR"
    REVIEWER = "REVIEWER"
    AUDITOR = "AUDITOR"

class ManuscriptStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_DESK_REVIEW = "UNDER_DESK_REVIEW"
    UNDER_PEER_REVIEW = "UNDER_PEER_REVIEW"
    REVISION_REQUESTED = "REVISION_REQUESTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class ManuscriptSubmission(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    abstract: str = Field(..., min_length=20)
    keywords: List[str] = Field(..., min_length=1)
    author_email: str
    file_hash_sha256: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

class ReviewerScorecard(BaseModel):
    methodology_score: int = Field(..., ge=1, le=5)
    clarity_score: int = Field(..., ge=1, le=5)
    reproducibility_score: int = Field(..., ge=1, le=5)
    comments_for_author: str
    confidential_comments_for_editor: Optional[str] = None
    recommendation: str = Field(..., pattern="^(ACCEPT|REVISE|REJECT)$")

class EditorialDecision(BaseModel):
    decision: ManuscriptStatus
    rationale: str

class ManuscriptRecord(BaseModel):
    id: str
    submission: ManuscriptSubmission
    status: ManuscriptStatus
    version: int = 1
    assigned_editor: Optional[str] = None
    assigned_reviewers: List[str] = []
    reviews: List[Dict[str, Any]] = []
    audit_trail: List[Dict[str, str]] = []
    created_at_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
