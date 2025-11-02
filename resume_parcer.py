import pypdf 
import docx 
import io
from fastapi import UploadFile
async def parse_resume(file: UploadFile) -> str:
    
    # This function takes an uploaded file and tries to extract all its text.
    
    filename = file.filename # Get file's name to check its type.
    content = await file.read() # Read the file's raw byte content.
    text = "" # Create an empty string to store the text.

    # Try to parse the file based on its extension.
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

    # If parsing fails for any reason, catch the error.
    except Exception as e:
        print(f"Error parsing... {e}")
        text = f"ERROR_PARSING_FILE: {filename}"
    
    return text