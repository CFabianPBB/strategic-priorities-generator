from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

# Import your existing functionality
from ai_processing import generate_strategic_priorities
from file_downloads import create_word, create_excel

class OrgData(BaseModel):
    org_name: str
    org_website: str

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Strategic Priorities Generator API"}

@app.post("/generate")
async def generate_priorities_endpoint(data: OrgData):
    # Call your existing AI processing function
    try:
        # Use your AI-powered function
        priorities = generate_strategic_priorities(data.org_name, data.org_website)
        return {"priorities": priorities}
    except Exception as e:
        # If there's an error with the AI, fall back to mock data
        print(f"Error with AI processing: {e}")
        # Your existing mock data as fallback
        priorities = [
            {
                "priority": "Safe and Secure Communities",
                "description": f"Ensuring public safety and justice for all residents of {data.org_name} by protecting communities from crime and harm while upholding fairness and accountability in the justice system.",
                "definitions": [
                    {
                        "title": "Effective & Equitable Law Enforcement:",
                        "description": "Prevent crime and respond quickly to emergencies through community-oriented policing and accountable practices that build public trust."
                    },
                    # ... other definitions ...
                ]
            },
            # ... other priorities ...
        ]
        return {"priorities": priorities}

@app.get("/download/word")
async def download_word_endpoint():
    # Call your existing word creation function
    try:
        file_path = create_word()
        return FileResponse(
            path=file_path,
            filename="strategic_priorities.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        print(f"Error creating Word document: {e}")
        return {"error": "Failed to create Word document"}

@app.get("/download/excel")
async def download_excel_endpoint():
    # Call your existing excel creation function
    try:
        file_path = create_excel()
        return FileResponse(
            path=file_path,
            filename="strategic_priorities.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        print(f"Error creating Excel document: {e}")
        return {"error": "Failed to create Excel document"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)