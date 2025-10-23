"""
Progress Tracking System for BCOS.

Provides real-time progress updates during analysis execution.
"""

from typing import Callable, Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum


class ProgressStatus(Enum):
    """Progress event status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ProgressLevel(Enum):
    """Level of progress granularity."""
    PHASE = "phase"          # Phase 1, Phase 2
    TASK = "task"            # Individual tasks
    SKILL = "skill"          # Skill execution
    API = "api"              # API calls
    LLM = "llm"              # LLM operations
    ACTION = "action"        # Generic actions


@dataclass
class ProgressEvent:
    """Represents a single progress event."""
    task_id: str
    task_name: str
    action: str
    status: ProgressStatus
    level: ProgressLevel
    timestamp: datetime = field(default_factory=datetime.now)
    details: Optional[Dict[str, Any]] = None


class ProgressTracker:
    """
    Tracks analysis progress and provides real-time updates.

    Features:
    - Task completion tracking
    - Estimated time remaining
    - Detailed action logging
    - Callback system for UI updates
    """

    def __init__(self, total_tasks: int, callback: Optional[Callable] = None):
        """
        Initialize progress tracker.

        Args:
            total_tasks: Total number of tasks to execute
            callback: Optional callback function called on each event
        """
        self.total_tasks = total_tasks
        self.callback = callback

        # Event tracking
        self.events: List[ProgressEvent] = []
        self.tasks: Dict[str, Dict[str, Any]] = {}

        # Timing
        self.start_time = datetime.now()
        self.task_start_times: Dict[str, datetime] = {}
        self.task_durations: List[float] = []  # Completed task durations in seconds

        # Current state
        self.current_phase = ""
        self.completed_tasks = 0
        self.failed_tasks = 0

    def emit(self,
             task_id: str,
             task_name: str,
             action: str,
             status: ProgressStatus,
             level: ProgressLevel = ProgressLevel.TASK,
             details: Optional[Dict[str, Any]] = None):
        """
        Emit a progress event.

        Args:
            task_id: Unique task identifier
            task_name: Human-readable task name
            action: Current action description
            status: Progress status
            level: Granularity level of event
            details: Optional additional details
        """
        event = ProgressEvent(
            task_id=task_id,
            task_name=task_name,
            action=action,
            status=status,
            level=level,
            details=details
        )

        self.events.append(event)

        # Update task tracking
        if task_id not in self.tasks:
            self.tasks[task_id] = {
                'name': task_name,
                'status': status,
                'actions': [],
                'start_time': None,
                'end_time': None
            }

        task = self.tasks[task_id]
        task['status'] = status
        task['actions'].append({
            'action': action,
            'level': level,
            'timestamp': event.timestamp
        })

        # Track task timing
        if status == ProgressStatus.IN_PROGRESS and task['start_time'] is None:
            task['start_time'] = event.timestamp
            self.task_start_times[task_id] = event.timestamp

        elif status == ProgressStatus.COMPLETED:
            if task['start_time']:
                task['end_time'] = event.timestamp
                duration = (event.timestamp - task['start_time']).total_seconds()
                self.task_durations.append(duration)

            self.completed_tasks += 1

        elif status == ProgressStatus.FAILED:
            self.failed_tasks += 1

        # Call callback for UI update
        if self.callback:
            self.callback(self.get_status())

    def set_phase(self, phase: str):
        """Set current phase (e.g., 'Phase 1', 'Phase 2')."""
        self.current_phase = phase
        if self.callback:
            self.callback(self.get_status())

    def get_status(self) -> Dict[str, Any]:
        """
        Get current progress status for UI display.

        Returns:
            Dictionary with current status information
        """
        # Calculate progress
        total_completed = self.completed_tasks + self.failed_tasks
        progress_percent = (total_completed / self.total_tasks * 100) if self.total_tasks > 0 else 0

        # Get current action (most recent event)
        current_action = None
        if self.events:
            latest = self.events[-1]
            if latest.status == ProgressStatus.IN_PROGRESS:
                current_action = {
                    'task_id': latest.task_id,
                    'task_name': latest.task_name,
                    'action': latest.action,
                    'level': latest.level.value
                }

        # Build task list with status
        task_list = []
        for task_id, task_info in self.tasks.items():
            task_list.append({
                'id': task_id,
                'name': task_info['name'],
                'status': task_info['status'].value,
                'actions': task_info['actions'][-5:]  # Last 5 actions
            })

        return {
            'phase': self.current_phase,
            'total_tasks': self.total_tasks,
            'completed': self.completed_tasks,
            'failed': self.failed_tasks,
            'in_progress': total_completed < self.total_tasks,
            'progress_percent': progress_percent,
            'current_action': current_action,
            'tasks': task_list,
            'eta': self.get_estimated_time_remaining(),
            'elapsed': self.get_elapsed_time()
        }

    def get_estimated_time_remaining(self) -> str:
        """
        Calculate estimated time remaining based on average task duration.

        Returns:
            Formatted time string (e.g., "2 minutes 30 seconds")
        """
        if not self.task_durations:
            return "Calculating..."

        # Calculate average task duration
        avg_duration = sum(self.task_durations) / len(self.task_durations)

        # Estimate remaining time
        remaining_tasks = self.total_tasks - self.completed_tasks - self.failed_tasks
        estimated_seconds = avg_duration * remaining_tasks

        if estimated_seconds < 0:
            return "Almost done..."

        # Format duration
        return self._format_duration(estimated_seconds)

    def get_elapsed_time(self) -> str:
        """Get formatted elapsed time since start."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return self._format_duration(elapsed)

    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to human-readable string."""
        if seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} {secs} seconds"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minutes"

    def get_task_history(self, task_id: str) -> List[Dict[str, Any]]:
        """Get full action history for a specific task."""
        if task_id in self.tasks:
            return self.tasks[task_id]['actions']
        return []
