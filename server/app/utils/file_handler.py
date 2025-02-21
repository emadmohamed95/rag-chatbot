import os
import shutil
import tempfile
from typing import Optional
from pathlib import Path


class FileHandler:
    """A context manager for handling temporary file operations"""
    
    def __init__(self, prefix: str = "upload_", base_dir: Optional[str] = None):
        """
        Initialize the FileHandler
        
        Args:
            prefix (str): Prefix for the temporary directory name
            base_dir (Optional[str]): Base directory for creating temp dir. If None, uses system temp
        """
        self.prefix = prefix
        self.base_dir = base_dir
        self.temp_dir: Optional[str] = None
        
    def __enter__(self) -> Path:
        """Create and return path to temporary directory"""
        self.temp_dir = tempfile.mkdtemp(prefix=self.prefix, dir=self.base_dir)
        return Path(self.temp_dir)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up temporary directory and its contents"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
    def get_temp_dir(self) -> Optional[Path]:
        """Get the current temporary directory path"""
        return Path(self.temp_dir) if self.temp_dir else None 