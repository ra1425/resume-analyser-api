from fastapi import FastAPI, File, UploadFile, Depends, Form, Request
from sqlalchemy.orm import Session
import json
import time

# Import custom files
import resume_parcer
import llm_analyzer
from database import AnalysisLog, get_db

# Imports for HTML
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI()

# Directions to HTML template
templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    # Find index.html and return it.
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analysis_resume/")
async def analyse_resume_endpoint(
    request: Request,
    resume: UploadFile = File(...), 
    job_description: str = Form(...), 
    db: Session = Depends(get_db)
):    
    # Stage 1: Parse
    resume_text = await resume_parcer.parse_resume(resume)
    jd_text = job_description

    if "ERROR" in resume_text or "UNSUPPORTED" in resume_text:
        return {"error": f"Failed to parse resume: {resume_text}"}
    
    # Stage 2: Analyse
    full_prompt = llm_analyzer.create_full_analysis_prompt(resume_text, jd_text)
    response_str = llm_analyzer.get_llm_analysis(full_prompt)

    try:
        # Clean JSON response
        clean_json_str = response_str[response_str.find('{') : response_str.rfind('}')+1]
        # Parse the  clean JSON response
        full_json = json.loads(clean_json_str)

        # Extract the two parts from it
        gap_json = full_json["gap_analysis"]
        tailor_json = full_json["resume_tailor"]

    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return {"error": "Failed to get a valid JSON response from the AI"}
    
    # Stage 3: Store
    new_log = AnalysisLog(
        raw_resume_text = resume_text, 
        raw_job_text = jd_text, 
        gaps_analysis = gap_json, 
        response_to_resume=tailor_json
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    # Stage 4: Respond
    return templates.TemplateResponse("results.html", {
        "request": request,  # Pass the request object
        "log_id": new_log.id,
        "gap_analysis": gap_json,
        "generated_content": tailor_json
    })