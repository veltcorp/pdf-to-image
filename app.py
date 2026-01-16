from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import subprocess
import tempfile
import os
import zipfile
import io

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

        # Cria o ZIP em memória (não depende do /tmp depois)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for name in sorted(os.listdir(tmp)):
                if name.endswith(".png"):
                    z.write(os.path.join(tmp, name), arcname=name)

        buf.seek(0)

        return StreamingResponse(
            buf,
            media_type="application/zip",
            headers={"Content-Disposition": 'attachment; filename="pages.zip"'}
        )
