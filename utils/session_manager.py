"""
Session management for BCOS.

Provides session-based output isolation to support multiple concurrent
and historical analyses without conflicts.
"""

import uuid
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import re


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


class SessionManager:
    """
    Manages analysis sessions and output organization.

    Each analysis gets:
    - Unique session ID
    - Dedicated output directory
    - Metadata tracking
    """

    def __init__(self, base_output_dir: str = "outputs"):
        """
        Initialize session manager.

        Args:
            base_output_dir: Base directory for all outputs
        """
        self.base_output_dir = Path(base_output_dir)
        self.base_output_dir.mkdir(exist_ok=True)

        self.manifest_file = self.base_output_dir / "manifest.json"
        self.manifest = self._load_manifest()

    def create_session(
        self,
        company_name: str,
        user_context: str = None
    ) -> Dict[str, Any]:
        """
        Create a new analysis session.

        Args:
            company_name: Name of the company being analyzed
            user_context: Optional user-provided context

        Returns:
            Session metadata
        """
        session_id = str(uuid.uuid4())[:8]  # Short UUID
        company_slug = slugify(company_name)
        timestamp = datetime.now()

        # Create session directory
        session_dir = self.base_output_dir / company_slug / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        session = {
            'session_id': session_id,
            'company_name': company_name,
            'company_slug': company_slug,
            'user_context': user_context,
            'created_at': timestamp.isoformat(),
            'status': 'running',
            'output_dir': str(session_dir),
            'files': {}
        }

        # Add to manifest
        if company_slug not in self.manifest:
            self.manifest[company_slug] = []

        self.manifest[company_slug].append(session)
        self._save_manifest()

        return session

    def update_session(
        self,
        session_id: str,
        company_slug: str,
        updates: Dict[str, Any]
    ):
        """
        Update session metadata.

        Args:
            session_id: Session ID
            company_slug: Company slug
            updates: Dictionary of updates
        """
        if company_slug in self.manifest:
            for session in self.manifest[company_slug]:
                if session['session_id'] == session_id:
                    session.update(updates)
                    if 'completed_at' in updates:
                        session['status'] = 'completed'
                    self._save_manifest()
                    return

    def get_session_dir(self, session_id: str, company_slug: str) -> Path:
        """Get output directory for a session."""
        return self.base_output_dir / company_slug / session_id

    def list_sessions(self, company_slug: str = None) -> List[Dict[str, Any]]:
        """
        List all sessions, optionally filtered by company.

        Args:
            company_slug: Optional company slug to filter

        Returns:
            List of session metadata
        """
        if company_slug:
            return self.manifest.get(company_slug, [])

        # Return all sessions
        all_sessions = []
        for sessions in self.manifest.values():
            all_sessions.extend(sessions)

        # Sort by creation date (newest first)
        all_sessions.sort(key=lambda x: x['created_at'], reverse=True)
        return all_sessions

    def get_session(self, session_id: str, company_slug: str) -> Optional[Dict[str, Any]]:
        """Get specific session metadata."""
        if company_slug in self.manifest:
            for session in self.manifest[company_slug]:
                if session['session_id'] == session_id:
                    return session
        return None

    def _load_manifest(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load session manifest from disk."""
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_manifest(self):
        """Save session manifest to disk."""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def add_output_file(
        self,
        session_id: str,
        company_slug: str,
        file_type: str,
        file_path: str
    ):
        """
        Register an output file for a session.

        Args:
            session_id: Session ID
            company_slug: Company slug
            file_type: Type of file (json, markdown, pdf, etc.)
            file_path: Path to the file
        """
        if company_slug in self.manifest:
            for session in self.manifest[company_slug]:
                if session['session_id'] == session_id:
                    session['files'][file_type] = file_path
                    self._save_manifest()
                    return
