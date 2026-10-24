from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from flask import current_app

from app.exceptions import ResumeUploadError
from app.utils.validators import secure_filename


class ResumeService:
    def __init__(self, upload_folder: str | None = None):
        self.upload_folder = upload_folder or current_app.config.get('UPLOAD_FOLDER', 'uploads/resumes')

    def validate_file(self, file_storage: Any) -> None:
        if not file_storage or not getattr(file_storage, 'filename', None):
            raise ResumeUploadError('Resume file is required')
        allowed = {'pdf', 'doc', 'docx'}
        name = file_storage.filename.lower()
        ext = name.rsplit('.', 1)[-1] if '.' in name else ''
        if ext not in allowed:
            raise ResumeUploadError('Unsupported resume format')
        content_type = (getattr(file_storage, 'mimetype', '') or '').lower()
        allowed_mimes = {
            'pdf': {'application/pdf', 'application/octet-stream'},
            'doc': {'application/msword', 'application/octet-stream'},
            'docx': {
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/octet-stream',
            },
        }
        if content_type and content_type not in allowed_mimes[ext]:
            raise ResumeUploadError('Resume content type does not match its file extension')
        if file_storage.content_length and file_storage.content_length > current_app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024):
            raise ResumeUploadError('Resume size exceeds the limit')

    def save_resume(self, file_storage: Any, candidate_id: str) -> Dict[str, Any]:
        self.validate_file(file_storage)
        folder = Path(current_app.root_path).parent / self.upload_folder
        folder.mkdir(parents=True, exist_ok=True)
        original_name = file_storage.filename
        safe_name = secure_filename(original_name)
        unique_name = f'{candidate_id}_{uuid4().hex}_{safe_name}'
        file_path = folder / unique_name
        file_storage.save(str(file_path))
        return {
            'id': __import__('uuid').uuid4().hex,
            'candidate_id': candidate_id,
            'filename': unique_name,
            'original_name': original_name,
            'content_type': 'application/octet-stream',
            'size': file_path.stat().st_size,
            'path': str(file_path),
            'created_at': datetime.utcnow().isoformat(),
        }

    def get_resume_path(self, resume_id: str, candidate_id: str) -> Optional[Path]:
        from app.repositories.base_repository import BaseRepository
        repo = BaseRepository()
        repo.collection_name = 'resumes'
        resume_record = repo.find_by_id(resume_id)
        if not resume_record or resume_record.get('candidate_id') != candidate_id:
            return None
        return Path(resume_record['path'])
