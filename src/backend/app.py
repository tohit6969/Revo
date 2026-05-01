import os
import subprocess
from fastapi import FastAPI, UploadFile, File, HTTPException

# ... existing imports and CORS setup ...

@app.post("/tryon")
async def tryon(file: UploadFile = File(...)):
    # 1) Save uploaded image
    contents = await file.read()
    tmp_dir   = "tmp"
    os.makedirs(tmp_dir, exist_ok=True)
    img_path  = os.path.join(tmp_dir, file.filename)
    with open(img_path, "wb") as f:
        f.write(contents)

    # 2) Call inference script via subprocess
    output_dir = os.path.join(tmp_dir, "meshes")
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "python",
        os.path.abspath("../../inference/run_inference.py"),
        "--input",  img_path,
        "--output", output_dir,
    ]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference error: {e.stderr}"
        )

    # 3) Parse the mesh path from stdout
    mesh_path = result.stdout.strip()
    if not os.path.isfile(mesh_path):
        raise HTTPException(status_code=500, detail="Mesh not generated")

    # 4) Expose the mesh via static files
    #    Copy or move mesh into your backend's static folder
    static_dir = "static/meshes"
    os.makedirs(static_dir, exist_ok=True)
    mesh_filename = os.path.basename(mesh_path)
    static_path   = os.path.join(static_dir, mesh_filename)
    os.replace(mesh_path, static_path)

    mesh_url = f"{os.getenv('BACKEND_URL')}/static/meshes/{mesh_filename}"
    return {"mesh_url": mesh_url}
