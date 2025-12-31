import shutil
import os
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import User, File, ChatSession
from ..dependencies import get_current_user

router = APIRouter(prefix="/files", tags=["files"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=File)
def upload_file(
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Validate file type
    if not file.filename.endswith((".csv", ".xlsx", ".xls", ".pdf", ".txt", ".epub")):
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: CSV, Excel, PDF, TXT, EPUB")

    # Create user directory
    user_dir = os.path.join(UPLOAD_DIR, str(current_user.id))
    os.makedirs(user_dir, exist_ok=True)
    
    file_location = os.path.join(user_dir, file.filename)
    
    # Save file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Save to DB
    db_file = File(
        filename=file.filename,
        filepath=file_location,
        owner_id=current_user.id
    )
    session.add(db_file)
    session.commit()
    session.refresh(db_file)
    return db_file

@router.get("/", response_model=List[File])
def list_files(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(File).where(File.owner_id == current_user.id)
    results = session.exec(statement)
    return results.all()

@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    file = session.get(File, file_id)
    if not file or file.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="File not found")
        
    # Remove from FS
    if os.path.exists(file.filepath):
        try:
            os.remove(file.filepath)
        except OSError:
            pass # Log error
            
    session.delete(file)
    session.commit()
    return {"ok": True}
