import pypdf 
import docx 
import io
from fastapi import UploadFile

async def parse_resume(file: UploadFile) -> str:
    
    # Parse the uploaded resume file and extract text content.
    
    filename = file.filename()
    content = await file.read()
    text = ""

    try:
        if filename.endswith('.pdf'):
            stream = io.BytesIO(content)
            reader = pypdf.PdfReader(stream)

            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        elif filename.endswith('.docx'):
            stream = io.BytesIO(content)
            reader = docx.Document(stream)

            for paragraph in reader.paragraphs:
                text += paragraph.text + "\n"

        elif filename.endswith('.txt'):
            text = content.decode("utf-8")
        
        else:
            text = f"UNSUPPORTED_FILE_TYPE: {filename}"
    except Exception as e:
        print(f"Error parsing... {e}")
        text = f"ERROR_PARSING_FILE: {filename}"
    
    return text

    