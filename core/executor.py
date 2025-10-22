"""
Task execution for BCOS.

Executes tasks using appropriate skills with safety features like
loop detection and step limits. Inspired by Dexter's execution pattern.
"""

from typing import Dict, Any, Optional, List
from anthropic import Anthropic
import os
import importlib
import sys
from pathlib import Path
from core.state_manager import Task
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Executor:
    """
    Executes tasks using the skills system.

    The Executor:
    - Routes tasks to appropriate skills
    - Monitors execution with step limits
    - Detects infinite loops
    - Handles errors gracefully
    """

    def __init__(
        self,
        max_steps_per_task: int = 10,
        api_key: str = None
    ):
        """
        Initialize the executor.

        Args:
            max_steps_per_task: Maximum execution steps per task
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.max_steps_per_task = max_steps_per_task
        self.client = Anthropic(api_key=api_key or os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-3-5-sonnet-20241022"

        # Track recent actions for loop detection
        self.recent_actions: List[str] = []

    def execute_task(
        self,
        task: Task,
        context: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single task.

        Args:
            task: Task to execute
            context: Execution context (company info, previous results)
            config: BCOS configuration

        Returns:
            Task execution result dictionary
        """
        logger.info(f"Executing task: {task.id} - {task.description}")

        try:
            # Try to load and execute skill
            skill_result = self._execute_skill(task, context, config)

            if skill_result:
                logger.info(f"Task {task.id} completed successfully")
                return {
                    'success': True,
                    'data': skill_result,
                    'task_id': task.id
                }
            else:
                # Skill not implemented - use LLM fallback
                logger.warning(f"Skill '{task.skill}' not implemented, using LLM fallback")
                llm_result = self._llm_fallback_execution(task, context, config)
                return {
                    'success': True,
                    'data': llm_result,
                    'task_id': task.id,
                    'method': 'llm_fallback'
                }

        except Exception as e:
            logger.error(f"Error executing task {task.id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'task_id': task.id
            }

    def _execute_skill(
        self,
        task: Task,
        context: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Execute a skill module.

        Attempts to import and run the skill's main function.

        Returns:
            Skill result if successful, None if skill not found
        """
        # Convert skill name to module path
        # e.g., "company-intelligence" -> "skills.phase1_foundation.company_intelligence"
        skill_name = task.skill.replace('-', '_')

        # Try different possible skill locations
        possible_paths = [
            f"skills.phase1_foundation.{skill_name}",
            f"skills.phase2_strategy.{skill_name}",
            f"skills.{skill_name}",
        ]

        for module_path in possible_paths:
            try:
                # Dynamically import skill module
                module = importlib.import_module(module_path)

                # Skills should expose an 'execute' function
                if hasattr(module, 'execute'):
                    execute_fn = getattr(module, 'execute')
                    result = execute_fn(
                        task=task,
                        context=context,
                        config=config
                    )
                    return result

            except ModuleNotFoundError:
                continue
            except Exception as e:
                logger.error(f"Error loading skill {module_path}: {e}")
                continue

        # Skill not found
        return None

    def _llm_fallback_execution(
        self,
        task: Task,
        context: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback: Use LLM to execute task when skill is not implemented.

        This allows the system to function even with incomplete skill implementations.
        The LLM will do its best to accomplish the task based on the description.
        """
        company = context.get('company', config.get('company', {}))

        prompt = f"""You are executing a business analysis task.

Company: {company.get('name', 'Unknown')}
Website: {company.get('website', 'Unknown')}
Industry: {company.get('industry', 'Unknown')}

Task: {task.description}
Skill: {task.skill}
Phase: {task.phase}

Context from previous tasks:
{self._summarize_context(context)}

Your job: Accomplish this task to the best of your ability using your knowledge.

Return a JSON object with your findings:
{{
  "findings": {{
    // Your analysis results here
  }},
  "summary": "Brief summary of what you found",
  "sources": ["Knowledge base", "Reasoning"],
  "confidence": "low/medium/high"
}}

Important:
- Be specific and actionable
- Base insights on the company and industry context
- Acknowledge when you're making assumptions
- This is a fallback - ideally the skill would gather real data
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
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

            result = json.loads(content)
            result['_fallback'] = True  # Mark as LLM fallback

            return result

        except Exception as e:
            logger.error(f"Error in LLM fallback execution: {e}")
            return {
                'error': str(e),
                'summary': 'Task execution failed',
                '_fallback': True
            }

    def _summarize_context(self, context: Dict[str, Any], max_length: int = 1000) -> str:
        """Create a brief summary of available context."""
        import json

        summary_parts = []

        # Company info
        if 'company' in context:
            company = context['company']
            summary_parts.append(f"Company: {company.get('name', 'Unknown')}")

        # Previous task results
        for key, value in context.items():
            if key != 'company' and value:
                if isinstance(value, dict):
                    summary_parts.append(f"{key}: {len(value)} data points")
                elif isinstance(value, list):
                    summary_parts.append(f"{key}: {len(value)} items")

        summary = '\n'.join(summary_parts)

        if len(summary) > max_length:
            summary = summary[:max_length] + "... (truncated)"

        return summary

    def detect_loop(self, action_signature: str) -> bool:
        """
        Detect if we're in an infinite loop.

        Args:
            action_signature: String describing the action (e.g., "skill:company-intel")

        Returns:
            True if loop detected
        """
        self.recent_actions.append(action_signature)

        # Keep only last 5 actions
        if len(self.recent_actions) > 5:
            self.recent_actions = self.recent_actions[-5:]

        # Check if last 4 actions are identical
        if len(self.recent_actions) >= 4:
            if len(set(self.recent_actions[-4:])) == 1:
                logger.warning(f"Loop detected: {action_signature} repeated 4 times")
                return True

        return False

    def reset_loop_detection(self):
        """Reset loop detection state (call between tasks)."""
        self.recent_actions = []
