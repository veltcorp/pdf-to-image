from fastapi import FastAPI, UploadFile, File
import subprocess
import tempfile
import os
import zipfile

app = FastAPI()

@app.post("/pdf-to-png")
async def pdf_to_png(file: UploadFile = File(...)):
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = os.path.join(tmp, "input.pdf")
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        output_prefix = os.path.join(tmp, "page")

        subprocess.run([
            "pdftoppm",
            "-png",
            "-r", "200",
            pdf_path,
            output_prefix
        ], check=True)

        zip_path = os.path.join(tmp, "pages.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for name in os.listdir(tmp):
                if name.endswith(".png"):
                    zipf.write(os.path.join(tmp, name), name)

        return {
            "message": "ok",
            "pages": sorted([n for n in os.listdir(tmp) if n.endswith(".png")])
        }
