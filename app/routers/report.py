from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.report_service import build_usage_summary

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.get("/summary", response_model=schemas.UsageSummary)
def get_usage_summary(
    db: Session = Depends(get_db),
):
    # Get ALL calculations (no per-user filter)
    calculations = db.query(models.Calculation).all()

    summary = build_usage_summary(calculations)
    return summary
