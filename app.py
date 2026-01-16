from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import subprocess
import tempfile
import os
import zipfile

app = FastAPI()

@app.post("/pdf-to-png")
async def pdf_to_png(file: UploadFile = File(...), dpi: int = 200):
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = os.path.join(tmp, "input.pdf")
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        out_prefix = os.path.join(tmp, "page")

        subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi), pdf_path, out_prefix],
            check=True
        )

        zip_path = os.path.join(tmp, "pages.zip")
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for name in sorted(os.listdir(tmp)):
                if name.endswith(".png"):
                    z.write(os.path.join(tmp, name), arcname=name)

        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename="pages.zip"
        )
