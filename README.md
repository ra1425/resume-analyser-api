# AI-Powered Resume Analyzer

This is a comprehensive, full-stack web application I built to solve one of the most dull part of job hunting: tailoring a resume for every single application.

This tool doesn't just find keywords; it uses the OpenAI GPT-3.5-Turbo model to perform a deep analysis of a resume against a job description. It identifies gaps, finds matching skills, and then *generates* new, tailored content (like a summary and bullet points) to help a resume stand out.

This project was a deep dive into building a full-stack, AI-driven application from the ground up, focusing on backend API design, database management, and prompt engineering.

---

## Core Features

* **Clean Web Interface:** A user-friendly HTML frontend built with Jinja2 for server-side rendering.
* **Multi-Modal Inputs:**
    * **Resume:** Accepts `.pdf`, `.docx`, and `.txt` file uploads.
    * **Job Description:** Uses a simple text area for easy copy-pasting.
* **Deep AI Gap Analysis:** The AI model identifies:
    * `Matched Skills:` What the job requires that's already in your CV.
    * `Missing Gaps:` A clear list of key skills and requirements from the job that are not present on the resume.
* **AI Content Generation:** The AI actively helps you improve your resume by:
    * Writing a brand new 2-3 sentence professional summary.
    * Re-writing 3-5 of your existing bullet points to be more impactful and relevant to the job.
* **Persistent Storage:** Every analysis is saved to an SQLite database, proving the app's capability to handle persistent data.

---

## My Technology Stack & Skills

I built this project using a modern Python stack, demonstrating a wide range of skills.

### 1. Backend & API
* **FastAPI:** I chose FastAPI for its high-performance, asynchronous capabilities (ASGI). It's incredibly fast and its automatic docs (`/docs`) made simplifying the API testing.
* **Uvicorn:** The ASGI server I used to run the FastAPI application.
* **Jinja2:** Used for HTML templating. This allowed me to build a dynamic, server-rendered frontend directly from my Python backend, which is perfect for an app of this scale.

### 2. AI & LLM
* **OpenAI API:** I used the `gpt-3.5-turbo` model for its balance of speed, cost, and powerful analysis.
* **Prompt Engineering:** This was the core of the AI logic. I designed a sophisticated "master prompt" that instructs the AI to perform *two* complex tasks (analysis and generation) in one call and return a single, perfectly structured JSON object. This avoids rate-limiting and is much more efficient.
* **JSON Parsing:** I wrote robust error handling to parse the AI's JSON response, including a function to clean the string of any markdown (like ` ```json `) before parsing.

### 3. Database
* **SQLAlchemy (ORM):** I used the SQLAlchemy ORM to define my database schema (`AnalysisLog`) as a Python class. This is much cleaner and more maintainable than writing raw SQL.
* **SQLite:** I chose SQLite as the database engine. Its file-based, serverless nature made it the perfect choice for this project, allowing for easy setup and persistent data logging without a separate database server.

### 4. File Parsing
* **`pypdf` & `python-docx`:** To handle the multi-modal resume uploads, I used these libraries to extract clean text from both PDF and Word document byte streams.

### 5. Environment & Tooling
* **Git & GitHub:** I used Git for all version control, with a clear history of feature-based commits.
* **Virtual Environments (`venv`):** All dependencies are managed in a standard Python virtual environment, captured in `requirements.txt`.
* **`python-dotenv`:** I used this to securely manage my `OPENAI_API_KEY` by loading it from an ignored `.env` file instead of hard-coding it.

---

## How to Run This Project Locally

You can run this entire application on your local machine.

### 1. Prerequisites
* Python 3.9+
* An [OpenAI API Key](https://platform.openai.com/account/api-keys) with a valid payment method.

### 2. Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/resume-analyzer-api.git
    cd resume-analyzer-api
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install all required packages:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your API Key:**
    * Create a file in the main folder named `.env`
    * Add your API key to this file:
        ```
        OPENAI_API_KEY="sk-YourSecretKeyGoesHere"
        ```

### 3. Run the App
1.  **Start the server:**
    ```bash
    uvicorn main:app --reload
    ```
2.  **Open your browser:**
    * Go to **`http://127.0.0.1:8000`** to use the app.
    * You can also go to **`http://127.0.0.1:8000/docs`** to test the API directly.

---

## 📂 Project Structure

This project is organized to be clean, modular, and easy to understand.
```
├── main.py # The main FastAPI app: handles routing and ties everything together. 
├── llm_analyzer.py # The "brain": contains all prompt logic and OpenAI API calls. 
├── resume_parcer.py # The "parser": handles logic for reading .pdf, .docx, and .txt files. 
├── database.py # The "memory": defines the SQLAlchemy database model and session management. 
├── requirements.txt # A list of all Python package dependencies. 
├── .env # (You create this) Stores my secret API key. 
├── analysis_log.db # (Auto-generated) The SQLite database file. 
└── templates/ 
  ├── index.html # The homepage with the upload form. 
  └── results.html # The results page for displaying the AI analysis.
```
