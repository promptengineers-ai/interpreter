from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import subprocess
import os
import shutil
import tempfile

app = FastAPI()

class CodeExecutionRequest(BaseModel):
    packages: list[str] = []
    code: str
    env: dict = {}

@app.post("/execute")
def run_code(request: CodeExecutionRequest):
    try:
        # Install packages if any are provided
        if request.packages:
            subprocess.check_call([f"pip install {' '.join(request.packages)}"], shell=True)

        # Set environment variables
        for key, value in request.env.items():
            os.environ[key] = value

        # Write code to a temporary file
        code_file_path = "/tmp/temp_code.py"
        with open(code_file_path, "w") as code_file:
            code_file.write(request.code)

        # Run the code
        result = subprocess.run(["python", code_file_path], capture_output=True, text=True)

        # Uninstall packages if any were installed
        if request.packages:
            subprocess.check_call([f"pip uninstall -y {' '.join(request.packages)}"], shell=True)

        return {"status": "success", "output": result.stdout, "errors": result.stderr}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload")
async def create_upload_file(file: UploadFile):
    try:
        upload_dir = "/tmp/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_location = f"{upload_dir}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        return {"filename": file.filename, "location": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)