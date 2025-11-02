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


def create_full_analysis_prompt(resume_text: str, jd_text: str) -> str:
    # This is our new "master" prompt.
    # It asks the AI to return ONE JSON object with two nested keys.
    
    prompt = f"""
    Here is my resume:
    ---RESUME START---
    {resume_text}
    ---RESUME END---

    Here is the job description I am applying for:
    ---JOB DESCRIPTION START---
    {jd_text}
    ---JOB DESCRIPTION END---

    Your task is to perform a full analysis and return a single JSON object.
    The JSON object must have two main keys: "gap_analysis" and "resume_tailor".

    1.  For the "gap_analysis" key, provide:
        -   "matched_skills": A list of skills from the JD supported by the resume.
        -   "missing_gaps": A list of key requirements from the JD missing from the resume.
        -   "suggestion": A short summary on how to align the resume.
    
    2.  For the "resume_tailor" key, provide:
        -   "new_summary": A new 2-3 sentence professional summary tailored for this job.
        -   "revised_bullets": A list of 3-5 re-written bullet points from the resume.
    
    Please format your output as a clean JSON object ONLY, with the structure:
    {{
        "gap_analysis": {{...}},
        "resume_tailor": {{...}}
    }}
    """
    return prompt