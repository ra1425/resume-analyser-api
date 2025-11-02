from fastapi import File, UploadFile, Depends, FastAPI
from sqlalchemy.orm import Session
import json

# Import custom files
import resume_parcer
import llm_analyzer
from database import AnalysisLog, get_db

app = FastAPI()

@app.post("/analysis_resume/")
async def analyse_resume_endpoint(resume: UploadFile = File(...), job_description: UploadFile = File(...), db: Session = Depends(get_db)):
    # Stage 1: Parse
    resume_text = await resume_parcer.parse_resume(resume)
    jd_text = await resume_parcer.parse_resume(job_description)

    if "ERROR" in resume_text or "UNSUPPORTED" in resume_text:
        return {"error": f"Failed to parse resume: {resume_text}"}
    if "ERROR" in jd_text or "UNSUPPORTED" in jd_text:
        return {"error": f"Failed to parse job description: {jd_text}"}
        
    # Stage 2: Analyse
    gap_prompt = llm_analyzer.create_gap_analysis_prompt(resume_text, jd_text)
    tailor_prompt = llm_analyzer.create_resume_tailor_prompt(resume_text, jd_text)
    
    gap_response_str = llm_analyzer.get_llm_analysis(gap_prompt)
    tailor_response_str = llm_analyzer.get_llm_analysis(tailor_prompt)

    try:
        gap_json = json.loads(gap_response_str)
        tailor_json = json.loads(tailor_response_str)
    except Exception as e:
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
    return { "log_id": new_log.id, "gap_analysis": gap_json, "generated_content": tailor_json}
