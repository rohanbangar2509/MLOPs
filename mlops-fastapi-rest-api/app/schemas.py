from pydantic import BaseModel, Field

class StudentInput(BaseModel):
    study_hours: float = Field(..., ge=0, le=24, description="Average study hours per day")
    attendance_pct: float = Field(..., ge=0, le=100, description="Attendance percentage")
    previous_score: float = Field(..., ge=0, le=100, description="Previous academic score")
    assignments_completed: int = Field(..., ge=0, le=20, description="Completed assignments")
    sleep_hours: float = Field(..., ge=0, le=24, description="Average sleep hours per day")

class PredictionResponse(BaseModel):
    passed: int
    prediction: str
    probability: float
    model: str
