from fastapi import FastAPI, File, UploadFile, Form
import requests
import os
import shutil

app = FastAPI()
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/api/")
async def forward_request(question: str = Form(...), file: UploadFile = File(None)):
    try:
        files = {}
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            files["file"] = (file.filename, open(file_path, "rb"))
        
        # Forward request to the external API
        response = requests.post("https://tds-project2-six.vercel.app/api/", data={"question": question}, files=files)
        
        # Cleanup uploaded file
        if file:
            os.remove(file_path)
        
        return response.json()
    except Exception as e:
        print(e)
        return {"answer": "Error processing request"}
