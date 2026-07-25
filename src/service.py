import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from src.models import (
    ManuscriptSubmission, ManuscriptRecord, ManuscriptStatus,
    ReviewerScorecard, EditorialDecision, Role
)

class EditorialWorkflowService:
    def __init__(self):
        self.manuscripts: Dict[str, ManuscriptRecord] = {}
        self._seed_synthetic_pack()

    def _seed_synthetic_pack(self):
        """Seed neutral, open-source sample manuscripts for evaluation."""
        sub = ManuscriptSubmission(
            title="Distributed Consensus in High-Throughput Peer Networks",
            abstract="We propose a low-latency Byzantine fault-tolerant algorithm designed for asynchronous peer-to-peer telemetry systems.",
            keywords=["distributed systems", "consensus", "byzantine fault tolerance"],
            author_email="researcher@synthetic-univ.edu",
            file_hash_sha256="8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4"
        )
        rec = self.submit_manuscript(sub)
        self.assign_editor(rec.id, "editor@open-science-journal.org", actor_role=Role.EDITOR)

    def submit_manuscript(self, submission: ManuscriptSubmission) -> ManuscriptRecord:
        ms_id = f"MS-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc).isoformat()
        record = ManuscriptRecord(
            id=ms_id,
            submission=submission,
            status=ManuscriptStatus.SUBMITTED,
            audit_trail=[{"timestamp": now, "action": "SUBMITTED", "actor": submission.author_email}]
        )
        self.manuscripts[ms_id] = record
        return record

    def assign_editor(self, ms_id: str, editor_email: str, actor_role: Role) -> ManuscriptRecord:
        if actor_role not in (Role.EDITOR, Role.AUDITOR):
            raise PermissionError("Only editorial staff can assign editors.")
        if ms_id not in self.manuscripts:
            raise KeyError(f"Manuscript {ms_id} not found.")
            
        rec = self.manuscripts[ms_id]
        rec.assigned_editor = editor_email
        rec.status = ManuscriptStatus.UNDER_DESK_REVIEW
        rec.audit_trail.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": f"ASSIGNED_EDITOR:{editor_email}",
            "actor": editor_email
        })
        return rec

    def invite_reviewer(self, ms_id: str, reviewer_email: str, actor_role: Role) -> ManuscriptRecord:
        if actor_role != Role.EDITOR:
            raise PermissionError("Only editors can invite reviewers.")
        if ms_id not in self.manuscripts:
            raise KeyError(f"Manuscript {ms_id} not found.")
            
        rec = self.manuscripts[ms_id]
        if reviewer_email not in rec.assigned_reviewers:
            rec.assigned_reviewers.append(reviewer_email)
        rec.status = ManuscriptStatus.UNDER_PEER_REVIEW
        rec.audit_trail.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": f"INVITED_REVIEWER:{reviewer_email}",
            "actor": "EDITOR"
        })
        return rec

    def submit_review(self, ms_id: str, reviewer_email: str, scorecard: ReviewerScorecard, actor_role: Role) -> ManuscriptRecord:
        if actor_role != Role.REVIEWER:
            raise PermissionError("Only assigned reviewers can submit scorecards.")
        if ms_id not in self.manuscripts:
            raise KeyError(f"Manuscript {ms_id} not found.")
            
        rec = self.manuscripts[ms_id]
        if reviewer_email not in rec.assigned_reviewers:
            raise PermissionError(f"Reviewer {reviewer_email} is not assigned to {ms_id}.")
            
        review_entry = {
            "reviewer_email": reviewer_email,
            "scorecard": scorecard.model_dump(),
            "submitted_at_utc": datetime.now(timezone.utc).isoformat()
        }
        rec.reviews.append(review_entry)
        rec.audit_trail.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": f"SUBMITTED_SCORECARD:{scorecard.recommendation}",
            "actor": reviewer_email
        })
        return rec

    def make_decision(self, ms_id: str, decision: EditorialDecision, actor_role: Role) -> ManuscriptRecord:
        if actor_role != Role.EDITOR:
            raise PermissionError("Only editors can make editorial decisions.")
        if ms_id not in self.manuscripts:
            raise KeyError(f"Manuscript {ms_id} not found.")
            
        rec = self.manuscripts[ms_id]
        rec.status = decision.decision
        rec.audit_trail.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": f"EDITORIAL_DECISION:{decision.decision} - {decision.rationale}",
            "actor": "EDITOR"
        })
        return rec
