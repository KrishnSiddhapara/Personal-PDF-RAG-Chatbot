import hashlib
import os
import re
from typing import Tuple

def sanitize_filename(filename: str) -> str:
    """Sanitizes user-provided filename to prevent path traversal attacks."""
    # Remove directory paths
    base_name = os.path.basename(filename)
    # Remove non-alphanumeric characters except dots, dashes, underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_.-]', '_', base_name)
    # Ensure it ends with .pdf
    if not sanitized.lower().endswith('.pdf'):
        sanitized += '.pdf'
    return sanitized

def generate_document_id(content: bytes, original_filename: str) -> str:
    """Generates a deterministic document ID using SHA-256 of file content and filename."""
    hasher = hashlib.sha256()
    hasher.update(content)
    hasher.update(original_filename.encode('utf-8'))
    return hasher.hexdigest()[:16]

def validate_pdf_file(filename: str, content: bytes) -> Tuple[bool, str]:
    """Validates if file is a valid PDF."""
    if not filename.lower().endswith('.pdf'):
        return False, "File must have a .pdf extension."
    if len(content) == 0:
        return False, "Uploaded file is empty."
    if not content.startswith(b'%PDF-'):
        return False, "File header invalid. Must be a valid PDF document."
    return True, "Valid PDF"
