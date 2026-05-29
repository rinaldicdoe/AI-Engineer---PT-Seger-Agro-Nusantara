from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.report_service import generate_report

app = FastAPI(title="AI Auto-Report API", version="1.0.0")

class ReportRequest(BaseModel):
    start_date: str = Field(..., examples=["2026-05-11"])
    end_date: str = Field(..., examples=["2026-05-17"])
    output_format: str = Field("pdf", examples=["pdf"])

@app.get("/")
def home():
    return {"message": "AI Auto-Report API aktif. Buka /docs untuk testing."}

@app.post("/generate-report")
def create_report(req: ReportRequest):
    return generate_report(req.start_date, req.end_date, req.output_format)
