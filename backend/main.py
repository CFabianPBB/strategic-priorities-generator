from fastapi import FastAPI
from ai_processing import generate_strategic_priorities
from file_downloads import create_word, create_excel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Strategic Priorities Generator API"}

@app.post("/generate")
def generate_priorities(org_name: str, org_website: str):
    priorities = generate_strategic_priorities(org_name, org_website)
    return {"priorities": priorities}

@app.get("/download/word")
def download_word():
    return create_word()

@app.get("/download/excel")
def download_excel():
    return create_excel()
