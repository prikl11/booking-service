import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile


async def save_upload_file(
        file: UploadFile,
        directory: Path,
) -> str:
    """
    Generating a unique file name & saving it to disk
    """
    UPLOAD_DIR = Path(f"media/{directory}")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    extention = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{extention}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)