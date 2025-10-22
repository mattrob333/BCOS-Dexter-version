"""
Task planning for BCOS.

Uses LLM to decompose high-level business research goals into specific,
executable tasks. Inspired by Dexter's planning approach.
"""

from typing import Dict, Any, List
from anthropic import Anthropic
import os
from core.state_manager import Task
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Planner:
    """
    Plans task execution using LLM-based decomposition.

    The Planner breaks down Phase 1 (foundation building) and Phase 2
    (strategy analysis) into discrete tasks that can be executed by skills.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the planner.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.client = Anthropic(api_key=api_key or os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-3-5-sonnet-20241022"

    def plan_phase1_tasks(self, config: Dict[str, Any]) -> List[Task]:
        """
        Plan Phase 1 foundation-building tasks.

        Args:
            config: BCOS configuration dictionary

        Returns:
            List of Task objects for Phase 1
        """
        company = config['company']
        scope = config.get('scope', {})
        depth = scope.get('phase1_depth', 'comprehensive')

        prompt = f"""You are planning Phase 1 (Foundation Building) for a business context analysis.

Target Company: {company['name']}
Website: {company['website']}
Industry: {company['industry']}
Analysis Depth: {depth}

Phase 1 involves gathering foundational business intelligence across 6 key areas:
1. Company Intelligence - Basic company facts, products, business model
2. Business Model Canvas - BMC analysis of value proposition, customers, channels, etc.
3. Value Chain Analysis - Map activities from suppliers to customers
4. Organizational Structure - Leadership, teams, culture
5. Market Intelligence - Market size, trends, opportunities
6. Competitor Intelligence - Profile key competitors

Create a task list for Phase 1. For each task:
- Provide a clear description
- Identify which skill should execute it
- Note any dependencies on other tasks

Return ONLY a JSON array of tasks in this format:
[
  {{
    "id": "phase1_task_1",
    "description": "Gather basic company intelligence from website",
    "skill": "company-intelligence",
    "dependencies": []
  }},
  ...
]

Keep it practical - aim for 5-8 tasks total. Be specific about what each task should accomplish."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse LLM response
            import json
            content = response.content[0].text

            # Extract JSON from response (handle markdown code blocks)
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()

            task_dicts = json.loads(content)

            # Convert to Task objects
            tasks = []
            for task_dict in task_dicts:
                task = Task(
                    id=task_dict['id'],
                    description=task_dict['description'],
                    phase='phase1',
                    skill=task_dict['skill'],
                    dependencies=task_dict.get('dependencies', [])
                )
                tasks.append(task)

            logger.info(f"Planned {len(tasks)} tasks for Phase 1")
            return tasks

        except Exception as e:
            logger.error(f"Error planning Phase 1 tasks: {e}")
            # Fallback to default task plan
            return self._default_phase1_tasks()

    def plan_phase2_tasks(self, config: Dict[str, Any], phase1_context: Dict[str, Any]) -> List[Task]:
        """
        Plan Phase 2 strategy analysis tasks.

        Args:
            config: BCOS configuration dictionary
            phase1_context: Results from Phase 1 to inform planning

        Returns:
            List of Task objects for Phase 2
        """
        company = config['company']
        scope = config.get('scope', {})
        frameworks = scope.get('phase2_frameworks', [])

        # Summarize Phase 1 findings
        phase1_summary = self._summarize_phase1_context(phase1_context)

        prompt = f"""You are planning Phase 2 (Strategy Analysis) for a business context analysis.

Target Company: {company['name']}
Industry: {company['industry']}

Phase 1 Summary:
{phase1_summary}

Strategic Frameworks to Apply:
{', '.join(frameworks)}

Phase 2 involves applying strategic frameworks to generate insights and recommendations.

Create a task list for Phase 2. For each framework requested, create 1-2 specific tasks.

Return ONLY a JSON array of tasks in this format:
[
  {{
    "id": "phase2_task_1",
    "description": "Conduct SWOT analysis based on Phase 1 findings",
    "skill": "swot-analyzer",
    "dependencies": []
  }},
  ...
]

All Phase 2 tasks implicitly depend on Phase 1 completion. Be specific about what insights each framework should generate."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse LLM response
            import json
            content = response.content[0].text

            # Extract JSON from response
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()

            task_dicts = json.loads(content)

            # Convert to Task objects
            tasks = []
            for task_dict in task_dicts:
                task = Task(
                    id=task_dict['id'],
                    description=task_dict['description'],
                    phase='phase2',
                    skill=task_dict['skill'],
                    dependencies=task_dict.get('dependencies', [])
                )
                tasks.append(task)

            logger.info(f"Planned {len(tasks)} tasks for Phase 2")
            return tasks

        except Exception as e:
            logger.error(f"Error planning Phase 2 tasks: {e}")
            # Fallback to default task plan
            return self._default_phase2_tasks(frameworks)

    def _summarize_phase1_context(self, phase1_context: Dict[str, Any]) -> str:
        """Create a brief summary of Phase 1 findings."""
        summary_lines = []

        for category, data in phase1_context.items():
            if data and isinstance(data, dict):
                summary_lines.append(f"- {category}: {len(data)} insights gathered")

        return '\n'.join(summary_lines) if summary_lines else "Phase 1 context available"

    def _default_phase1_tasks(self) -> List[Task]:
        """Fallback: Return default Phase 1 task plan."""
        return [
            Task(
                id="phase1_task_1",
                description="Gather company intelligence from website and public sources",
                phase="phase1",
                skill="company-intelligence",
                dependencies=[]
            ),
            Task(
                id="phase1_task_2",
                description="Analyze business model using Business Model Canvas framework",
                phase="phase1",
                skill="business-model-canvas",
                dependencies=["phase1_task_1"]
            ),
            Task(
                id="phase1_task_3",
                description="Map company value chain from suppliers to customers",
                phase="phase1",
                skill="value-chain-mapper",
                dependencies=["phase1_task_1"]
            ),
            Task(
                id="phase1_task_4",
                description="Research market landscape and competitive dynamics",
                phase="phase1",
                skill="market-intelligence",
                dependencies=["phase1_task_1"]
            ),
            Task(
                id="phase1_task_5",
                description="Profile key competitors and their strategies",
                phase="phase1",
                skill="competitor-intelligence",
                dependencies=["phase1_task_4"]
            ),
        ]

    def _default_phase2_tasks(self, frameworks: List[str]) -> List[Task]:
        """Fallback: Return default Phase 2 task plan."""
        tasks = []
        task_id = 1

        framework_mapping = {
            'SWOT Analysis': 'swot-analyzer',
            'Porter\'s Five Forces': 'porters-five-forces',
            'BCG Matrix': 'bcg-matrix',
            'Blue Ocean Strategy': 'blue-ocean-strategy',
            'PESTEL Analysis': 'pestel-analyzer',
        }

        for framework in frameworks:
            skill = framework_mapping.get(framework, framework.lower().replace(' ', '-'))
            task = Task(
                id=f"phase2_task_{task_id}",
                description=f"Apply {framework} to generate strategic insights",
                phase="phase2",
                skill=skill,
                dependencies=[]
            )
            tasks.append(task)
            task_id += 1

        return tasks
