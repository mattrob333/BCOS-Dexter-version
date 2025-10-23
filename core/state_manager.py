"""
State management for BCOS.

Maintains business context and research findings across Phase 1 and Phase 2.
Enables context passing between different analysis stages.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path


@dataclass
class Task:
    """Represents a single task in the execution plan."""
    id: str
    description: str
    phase: str  # "phase1" or "phase2"
    skill: str  # Skill name to use
    dependencies: List[str] = field(default_factory=list)  # Task IDs this depends on
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            'id': self.id,
            'description': self.description,
            'phase': self.phase,
            'skill': self.skill,
            'dependencies': self.dependencies,
            'status': self.status,
            'result': self.result,
            'error': self.error,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }


class StateManager:
    """
    Manages the state and context throughout BCOS execution.

    Responsibilities:
    - Track Phase 1 findings (company intel, market data, competitor analysis)
    - Track Phase 2 insights (strategic frameworks, recommendations)
    - Maintain task execution history
    - Enable state persistence and recovery
    """

    def __init__(self):
        """Initialize empty state."""
        # Core company context
        self.company_name: str = ""
        self.company_website: str = ""
        self.industry: str = ""

        # Phase 1: Foundation data
        self.phase1_context: Dict[str, Any] = {
            'company_intelligence': {},      # Website scraping, company basics
            'business_model_canvas': {},     # BMC analysis
            'value_chain': {},               # Value chain mapping
            'org_structure': {},             # Organizational analysis
            'market_intelligence': {},       # Market landscape
            'competitor_intelligence': {},   # Competitor profiles
        }

        # Phase 2: Strategy insights
        self.phase2_context: Dict[str, Any] = {
            'swot': {},                      # SWOT analysis
            'porters_five_forces': {},       # Porter's Five Forces
            'bcg_matrix': {},                # BCG Matrix
            'blue_ocean': {},                # Blue Ocean Strategy
            'pestel': {},                    # PESTEL analysis
            'competitive_strategy': {},      # Competitive positioning
            'sales_intelligence': {},        # Sales playbooks
        }

        # Task tracking
        self.tasks: List[Task] = []
        self.current_phase: str = "phase1"

        # Execution metadata
        self.started_at: Optional[datetime] = None
        self.phase1_completed_at: Optional[datetime] = None
        self.phase2_completed_at: Optional[datetime] = None

    def set_company_context(self, name: str, website: str, industry: str):
        """Set the target company information."""
        self.company_name = name
        self.company_website = website
        self.industry = industry

    def add_task(self, task: Task):
        """Add a task to the execution plan."""
        self.tasks.append(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task_status(self, task_id: str, status: str, result: Dict[str, Any] = None, error: str = None):
        """Update task status and result."""
        task = self.get_task(task_id)
        if task:
            task.status = status
            if result:
                task.result = result
            if error:
                task.error = error
            if status == "in_progress" and not task.started_at:
                task.started_at = datetime.now()
            elif status in ["completed", "failed"]:
                task.completed_at = datetime.now()

    def get_phase1_context(self) -> Dict[str, Any]:
        """Get all Phase 1 context for use in Phase 2."""
        return {
            'company': {
                'name': self.company_name,
                'website': self.company_website,
                'industry': self.industry,
            },
            **self.phase1_context
        }

    def get_completed_tasks(self, phase: str = None) -> List[Task]:
        """Get all completed tasks, optionally filtered by phase."""
        completed = [t for t in self.tasks if t.status == "completed"]
        if phase:
            completed = [t for t in completed if t.phase == phase]
        return completed

    def get_pending_tasks(self, phase: str = None) -> List[Task]:
        """Get all pending tasks, optionally filtered by phase."""
        pending = [t for t in self.tasks if t.status == "pending"]
        if phase:
            pending = [t for t in pending if t.phase == phase]
        return pending

    def save_state(self, filepath: str):
        """Save current state to JSON file."""
        state_dict = {
            'company_name': self.company_name,
            'company_website': self.company_website,
            'industry': self.industry,
            'phase1_context': self.phase1_context,
            'phase2_context': self.phase2_context,
            'tasks': [t.to_dict() for t in self.tasks],
            'current_phase': self.current_phase,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'phase1_completed_at': self.phase1_completed_at.isoformat() if self.phase1_completed_at else None,
            'phase2_completed_at': self.phase2_completed_at.isoformat() if self.phase2_completed_at else None,
        }

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state_dict, f, indent=2, ensure_ascii=False)

    def load_state(self, filepath: str):
        """Load state from JSON file (for recovery)."""
        with open(filepath, 'r', encoding='utf-8') as f:
            state_dict = json.load(f)

        self.company_name = state_dict.get('company_name', '')
        self.company_website = state_dict.get('company_website', '')
        self.industry = state_dict.get('industry', '')
        self.phase1_context = state_dict.get('phase1_context', {})
        self.phase2_context = state_dict.get('phase2_context', {})
        self.current_phase = state_dict.get('current_phase', 'phase1')

        # Reconstruct tasks
        self.tasks = []
        for task_dict in state_dict.get('tasks', []):
            task = Task(
                id=task_dict['id'],
                description=task_dict['description'],
                phase=task_dict['phase'],
                skill=task_dict['skill'],
                dependencies=task_dict.get('dependencies', []),
                status=task_dict.get('status', 'pending'),
                result=task_dict.get('result'),
                error=task_dict.get('error'),
            )
            self.tasks.append(task)

    def get_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        total_tasks = len(self.tasks)
        completed = len([t for t in self.tasks if t.status == "completed"])
        failed = len([t for t in self.tasks if t.status == "failed"])
        pending = len([t for t in self.tasks if t.status == "pending"])

        return {
            'company': self.company_name,
            'current_phase': self.current_phase,
            'tasks': {
                'total': total_tasks,
                'completed': completed,
                'failed': failed,
                'pending': pending,
            },
            'started_at': self.started_at.isoformat() if self.started_at else None,
        }
