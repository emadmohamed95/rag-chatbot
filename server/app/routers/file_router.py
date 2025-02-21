from typing import List
from fastapi import APIRouter, UploadFile, File, Depends
from services.file_service import save_uploaded_files
from databases.qdrant import get_qdrant, Qdrant

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    qdrant: Qdrant = Depends(get_qdrant)
):
    """
    Upload multiple PDF files endpoint. Files will be processed and added to the vector store.
    
    Args:
        files: List of PDF files to upload
        qdrant: Qdrant instance from dependency injection
        
    Returns:
        dict: Processing results for each file
    """
    results = await save_uploaded_files(
        files=files,
        vector_store=qdrant.get_vector_store()
    )
    
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "failed"]
    
    return {
        "message": f"Processed {len(successful)} files successfully, {len(failed)} failed",
        "successful": successful,
        "failed": failed
    } 