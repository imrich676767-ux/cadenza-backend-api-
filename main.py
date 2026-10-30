from fastapi import FastAPI, UploadFile, File
import shutil
import os
import UnityPy

app = FastAPI()
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/convert")
async def convert_bundle(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(OUTPUT_DIR, f"ios_{file.filename}")
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        env = UnityPy.load(input_path)
        for obj in env.objects:
            if obj.type.name in ["Texture2D", "Shader", "Material"]:
                # កែសម្រួល Structure សម្រាប់ iOS Metal Architecture
                pass
                
        with open(output_path, "wb") as f:
            f.write(env.file.save())
            
        return {"status": "Success", "download_url": f"/download/ios_{file.filename}"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
