import os
import openai 
from dotenv import load_dotenv

# Loads the OPENAI_API_KEY 
load_dotenv() 
# Creates the client
client = openai.OpenAI() 


def get_llm_analysis(prompt: str) -> str:
    # Reusable function to call the AI.
    
    # Catching the error if the OpenAI server is down
    try:
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a world-class career coach and professional resume writer."},
                {"role": "user", "content": prompt} 
            ], 
            temperature = 0.2
        )
        return  response.choices[0].message.content
        
    except Exception as e:
        print(f"Error communicating with AI: {e}") 
        return "Error communicating with AI"


def create_gap_analysis_prompt(resume_text: str, jd_text: str) -> str:
    # This function builds a prompt for the AI model to find gaps in the CV. 
    
    prompt = f"""
    Here is my resume:
    ---RESUME START---
    {resume_text}
    ---RESUME END---

    Here is the job description I am applying for:
    ---JOB DESCRIPTION START---
    {jd_text}
    ---JOB DESCRIPTION END---

    Your task is to perform a detailed Gap Analysis. Compare my resume against the job description and provide:
    1.  **Matched Skills:** A list of key requirements from the JD that are strongly supported by my resume.
    2.  **Missing Gaps:** A list of key requirements (the "catch words") from the JD that are not clearly present on my resume.
    3.  **Suggestion for Improvement:** A short, actionable summary on how I could better align my resume.
    
    Please format your output as a clean JSON object ONLY, with the keys: "matched_skills", "missing_gaps", "suggestion".
    """
    return prompt

def create_resume_tailor_prompt(resume_text: str, jd_text: str) -> str:
    # This function builds a prompt for the AI model to reformulate the CV. 
    
    prompt = f"""
    Here is my resume:
    ---RESUME START---
    {resume_text}
    ---RESUME END---

    Here is the job description I am applying for:
    ---JOB DESCRIPTION START---
    {jd_text}
    ---JOB DESCRIPTION END---

    Your task is to act as a professional resume writer. 
    **Do not invent new experiences.** Instead, rephrase, re-order, and emphasize existing experiences and skills from the resume to highlight the applicant's fit for this specific job.

    Please generate:
    1.  **New Summary:** A new 2-3 sentence professional summary tailored for this job.
    2.  **Revised Bullets:** A list of 3-5 bullet points from my "Experience" section, re-written to include keywords and metrics relevant to the job description.
    
    Format your output as a clean JSON object ONLY, with the keys: "new_summary", "revised_bullets".
    """
    return prompt