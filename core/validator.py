"""
Task validation for BCOS.

Validates that tasks have been completed successfully before proceeding.
Prevents incomplete work from propagating through the system.
"""

from typing import Dict, Any, Optional
from anthropic import Anthropic
import os
from dotenv import load_dotenv
from core.state_manager import Task
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)


class Validator:
    """
    Validates task completion using LLM-based assessment.

    The Validator ensures that each task has actually accomplished its goal
    before marking it complete and moving to dependent tasks.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the validator.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.client = Anthropic(api_key=api_key or os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-3-7-sonnet-20250219"

    def validate_task_completion(
        self,
        task: Task,
        result: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Validate that a task has been completed successfully.

        Args:
            task: The task to validate
            result: The result produced by the task execution
            context: Additional context for validation

        Returns:
            Tuple of (is_valid, feedback)
            - is_valid: True if task is complete and valid
            - feedback: Optional message explaining validation result
        """
        # Basic validation: check if result exists and is non-empty
        if not result:
            return False, "Task produced no result"

        if isinstance(result, dict) and not result:
            return False, "Task produced empty result dictionary"

        # For certain task types, use LLM validation
        if self._should_use_llm_validation(task):
            return self._llm_validate(task, result, context)
        else:
            # Simple heuristic validation
            return self._heuristic_validate(task, result)

    def _should_use_llm_validation(self, task: Task) -> bool:
        """Determine if LLM validation is needed for this task."""
        # Use LLM for complex analysis tasks
        complex_skills = [
            'business-model-canvas',
            'value-chain-mapper',
            'swot-analyzer',
            'porters-five-forces',
            'bcg-matrix',
        ]
        return task.skill in complex_skills

    def _heuristic_validate(self, task: Task, result: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Simple heuristic validation without LLM.

        Checks for:
        - Non-empty result
        - Presence of expected keys
        - Reasonable data size
        """
        # Check for error field
        if result.get('error'):
            return False, f"Task reported error: {result['error']}"

        # Check for success indicator
        if 'success' in result and not result['success']:
            return False, "Task reported unsuccessful completion"

        # Check for meaningful data
        if 'data' in result:
            data = result['data']
            if isinstance(data, dict) and len(data) == 0:
                return False, "Task data is empty"
            if isinstance(data, list) and len(data) == 0:
                return False, "Task data list is empty"
            if isinstance(data, str) and len(data) < 10:
                return False, "Task data is too short"

        # If we get here, basic validation passed
        return True, "Task completed successfully"

    def _llm_validate(
        self,
        task: Task,
        result: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Use LLM to validate task completion.

        The LLM assesses whether the result actually fulfills the task requirements.
        """
        prompt = f"""You are validating task completion for a business analysis system.

Task: {task.description}
Skill Used: {task.skill}
Phase: {task.phase}

Result Summary:
{self._summarize_result(result)}

Your job: Determine if this task has been completed successfully.

Criteria:
1. Does the result address the task description?
2. Is the result substantive and useful?
3. Are there any obvious gaps or errors?

Respond with ONLY a JSON object:
{{
  "is_valid": true/false,
  "feedback": "Brief explanation of validation decision"
}}
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse LLM response
            import json
            content = response.content[0].text

            # Extract JSON
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()

            validation_result = json.loads(content)

            is_valid = validation_result.get('is_valid', False)
            feedback = validation_result.get('feedback', '')

            logger.info(f"LLM validation for {task.id}: valid={is_valid}")

            return is_valid, feedback

        except Exception as e:
            logger.error(f"Error in LLM validation: {e}")
            # Fallback to heuristic validation
            return self._heuristic_validate(task, result)

    def _summarize_result(self, result: Dict[str, Any], max_length: int = 500) -> str:
        """Create a brief summary of task result for validation."""
        import json

        result_str = json.dumps(result, indent=2)

        if len(result_str) > max_length:
            # Truncate but keep structure visible
            return result_str[:max_length] + "\n... (truncated)"

        return result_str

    def check_dependencies_met(self, task: Task, completed_task_ids: list[str]) -> bool:
        """
        Check if all task dependencies have been completed.

        Args:
            task: Task to check
            completed_task_ids: List of IDs of completed tasks

        Returns:
            True if all dependencies are met
        """
        if not task.dependencies:
            return True

        for dep_id in task.dependencies:
            if dep_id not in completed_task_ids:
                logger.debug(f"Task {task.id} waiting on dependency {dep_id}")
                return False

        return True
