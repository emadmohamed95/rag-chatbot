import os
from io import BytesIO
from pathlib import Path
from typing import List
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore


async def process_pdf_content(content: bytes, filename: str) -> str:
    """
    Extract text from PDF content in memory
    
    Args:
        content: PDF file content as bytes
        filename: Name of the file (for error reporting)
        
    Returns:
        Extracted text from the PDF
    """
    try:
        reader = PdfReader(BytesIO(content))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            # Add a newline between pages for better text splitting
            text += "\n\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing PDF file {filename}: {str(e)}")


def split_text(text: str) -> List[str]:
    """
    Split text into chunks using LangChain's RecursiveCharacterTextSplitter
    
    Args:
        text: Text to split
        
    Returns:
        List of text chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)


async def save_uploaded_files(files: List[UploadFile], vector_store: QdrantVectorStore) -> List[dict]:
    """
    Process uploaded PDF files and add their content to Qdrant
    
    Args:
        files: List of FastAPI UploadFile objects
        vector_store: QdrantVectorStore instance for storing embeddings
        
    Returns:
        List of dictionaries containing file processing results
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
        
    results = []
    
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail=f"File {file.filename} is not a PDF file"
            )
        
        # Read file content
        content = await file.read()
        
        try:
            # Process PDF directly from memory
            text = await process_pdf_content(content, file.filename)
            
            # Skip empty documents
            if not text.strip():
                results.append({
                    "filename": file.filename,
                    "error": "No text content found in PDF",
                    "status": "failed"
                })
                continue
                
            chunks = split_text(text)
            
            # Add to Qdrant
            try:
                vector_store.add_texts(
                    texts=chunks,
                    metadatas=[{
                        "source": file.filename,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    } for i in range(len(chunks))]
                )
                
                results.append({
                    "filename": file.filename,
                    "chunks_processed": len(chunks),
                    "total_characters": len(text),
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "error": str(e),
                    "status": "failed"
                })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e),
                "status": "failed"
            })
        finally:
            # Reset file pointer for potential reuse
            await file.seek(0)
            
    return results 