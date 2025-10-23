"""
Main orchestrator for BCOS.

Coordinates the entire business context analysis workflow using a
Dexter-inspired multi-agent pattern.
"""

from typing import Dict, Any, Optional, Callable
from datetime import datetime
from core.planner import Planner
from core.executor import Executor
from core.validator import Validator
from core.state_manager import StateManager, Task
from utils.logger import setup_logger
from utils.progress_tracker import ProgressStatus, ProgressLevel

logger = setup_logger(__name__)


class BusinessContextOrchestrator:
    """
    Main orchestrator for the Business Context OS.

    Coordinates Phase 1 (foundation building) and Phase 2 (strategy analysis)
    using a multi-agent pattern:
    - Planner: Decomposes goals into tasks
    - Executor: Executes tasks using skills
    - Validator: Validates task completion
    - StateManager: Maintains context across phases
    """

    def __init__(self, config: Dict[str, Any], progress_callback: Optional[Callable] = None):
        """
        Initialize the orchestrator.

        Args:
            config: BCOS configuration dictionary
            progress_callback: Optional callback for progress updates
        """
        self.config = config
        self.state = StateManager()
        self.progress_callback = progress_callback

        # Extract safety limits from config
        advanced = config.get('advanced', {})
        max_steps = advanced.get('max_steps', 50)
        max_steps_per_task = advanced.get('max_steps_per_task', 10)

        # Initialize agents
        self.planner = Planner()
        self.executor = Executor(max_steps_per_task=max_steps_per_task)
        self.validator = Validator()

        # Track execution
        self.max_steps = max_steps
        self.current_step = 0

        # Set company context
        company = config['company']
        self.state.set_company_context(
            name=company['name'],
            website=company['website'],
            industry=company['industry']
        )

        logger.info(f"Orchestrator initialized for {company['name']}")

    def _emit_progress(self,
                      task_id: str,
                      task_name: str,
                      action: str,
                      status: ProgressStatus,
                      level: ProgressLevel = ProgressLevel.TASK,
                      details: Optional[Dict[str, Any]] = None):
        """Emit progress event if callback is set."""
        if self.progress_callback:
            self.progress_callback(
                task_id=task_id,
                task_name=task_name,
                action=action,
                status=status,
                level=level,
                details=details
            )

    def run(self) -> Dict[str, Any]:
        """
        Run the BCOS analysis based on the analysis mode.

        Modes:
            - "business_overview": Run Phase 1 only (Business Overview)
            - "frameworks": Run Phase 2 only (requires existing Phase 1)
            - "full": Run both Phase 1 and Phase 2 (default)

        Returns:
            Final analysis results
        """
        self.state.started_at = datetime.now()
        analysis_mode = self.config.get('analysis_mode', 'full')

        try:
            if analysis_mode == "business_overview":
                # Run Phase 1 only
                return self.run_business_overview_only()

            elif analysis_mode == "frameworks":
                # Run Phase 2 only (requires existing Phase 1)
                return self.run_frameworks_only()

            else:
                # Run both phases (full analysis)
                return self.run_full_analysis()

        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            return {
                'error': str(e),
                'summary': self.state.get_summary()
            }

    def run_business_overview_only(self) -> Dict[str, Any]:
        """
        Run Phase 1 (Business Overview) only.

        Returns:
            Business Overview results
        """
        logger.info("=" * 60)
        logger.info("BUSINESS OVERVIEW ANALYSIS")
        logger.info("=" * 60)

        phase1_results = self.run_phase1()

        if not phase1_results:
            logger.error("Business Overview failed")
            return {'error': 'Business Overview failed'}

        self.state.phase1_completed_at = datetime.now()
        self.state.current_phase = "phase1_complete"

        results = {
            'company': self.state.company_name,
            'phase1': phase1_results,
            'phase2': {},
            'summary': self.state.get_summary(),
            'analysis_type': 'business_overview'
        }

        logger.info("=" * 60)
        logger.info("BUSINESS OVERVIEW COMPLETE")
        logger.info("=" * 60)

        return results

    def run_frameworks_only(self) -> Dict[str, Any]:
        """
        Run Phase 2 (Strategic Frameworks) only.
        Requires existing Phase 1 context to be loaded.

        Returns:
            Strategic framework results
        """
        logger.info("=" * 60)
        logger.info("STRATEGIC FRAMEWORKS ANALYSIS")
        logger.info("=" * 60)

        # TODO: Load existing Phase 1 context from session
        # For now, return error if Phase 1 context is empty
        if not self.state.phase1_context:
            logger.error("No Phase 1 context found - cannot run frameworks only")
            return {'error': 'Business Overview required before running frameworks'}

        self.state.current_phase = "phase2"

        phase2_results = self.run_phase2()

        self.state.phase2_completed_at = datetime.now()

        results = {
            'company': self.state.company_name,
            'phase1': self.state.phase1_context,  # Include existing Phase 1
            'phase2': phase2_results,
            'summary': self.state.get_summary(),
            'analysis_type': 'frameworks'
        }

        logger.info("=" * 60)
        logger.info("STRATEGIC FRAMEWORKS COMPLETE")
        logger.info("=" * 60)

        return results

    def run_full_analysis(self) -> Dict[str, Any]:
        """
        Run complete analysis (Phase 1 + Phase 2).

        Returns:
            Complete analysis results
        """
        # Phase 1: Foundation Building
        logger.info("=" * 60)
        logger.info("PHASE 1: FOUNDATION BUILDING")
        logger.info("=" * 60)

        phase1_results = self.run_phase1()

        if not phase1_results:
            logger.error("Phase 1 failed - cannot proceed to Phase 2")
            return {'error': 'Phase 1 failed', 'phase1_results': phase1_results}

        self.state.phase1_completed_at = datetime.now()
        self.state.current_phase = "phase2"

        # Phase 2: Strategy Analysis
        logger.info("=" * 60)
        logger.info("PHASE 2: STRATEGY ANALYSIS")
        logger.info("=" * 60)

        phase2_results = self.run_phase2()

        self.state.phase2_completed_at = datetime.now()

        # Return complete results
        results = {
            'company': self.state.company_name,
            'phase1': phase1_results,
            'phase2': phase2_results,
            'summary': self.state.get_summary(),
            'analysis_type': 'full'
        }

        logger.info("=" * 60)
        logger.info("ANALYSIS COMPLETE")
        logger.info("=" * 60)

        return results

    def run_phase1(self) -> Dict[str, Any]:
        """
        Execute Phase 1: Foundation Building.

        Returns:
            Phase 1 results dictionary
        """
        # Step 1: Plan tasks
        logger.info("Planning Phase 1 tasks...")
        tasks = self.planner.plan_phase1_tasks(self.config)

        for task in tasks:
            self.state.add_task(task)
            logger.info(f"  - {task.id}: {task.description}")

        # Step 2: Execute tasks
        logger.info(f"\nExecuting {len(tasks)} Phase 1 tasks...")

        completed_task_ids = []

        for task in tasks:
            if self.current_step >= self.max_steps:
                logger.warning(f"Reached max steps ({self.max_steps}) - stopping Phase 1")
                break

            # Check dependencies
            if not self.validator.check_dependencies_met(task, completed_task_ids):
                logger.info(f"Skipping {task.id} - dependencies not met")
                continue

            # Emit task start
            self._emit_progress(
                task_id=task.id,
                task_name=task.description,
                action=f"Starting {task.description}...",
                status=ProgressStatus.IN_PROGRESS,
                level=ProgressLevel.TASK
            )

            # Execute task
            self.state.update_task_status(task.id, "in_progress")
            self.executor.reset_loop_detection()

            # Emit skill loading
            skill_name = task.skill.replace('-', ' ').title()
            self._emit_progress(
                task_id=task.id,
                task_name=task.description,
                action=f"Loading {skill_name} skill...",
                status=ProgressStatus.IN_PROGRESS,
                level=ProgressLevel.SKILL
            )

            result = self.executor.execute_task(
                task=task,
                context=self.state.phase1_context,
                config=self.config
            )

            self.current_step += 1

            # Validate result
            is_valid, feedback = self.validator.validate_task_completion(task, result)

            if is_valid:
                # Store result in state
                self._store_phase1_result(task, result)
                self.state.update_task_status(task.id, "completed", result=result)
                completed_task_ids.append(task.id)
                logger.info(f"[OK] {task.id} completed successfully")

                # Emit task completion
                self._emit_progress(
                    task_id=task.id,
                    task_name=task.description,
                    action=f"✓ Completed {task.description}",
                    status=ProgressStatus.COMPLETED,
                    level=ProgressLevel.TASK
                )
            else:
                self.state.update_task_status(task.id, "failed", error=feedback)
                logger.warning(f"[X] {task.id} validation failed: {feedback}")

                # Emit task failure
                self._emit_progress(
                    task_id=task.id,
                    task_name=task.description,
                    action=f"✗ Failed: {feedback}",
                    status=ProgressStatus.FAILED,
                    level=ProgressLevel.TASK,
                    details={'error': feedback}
                )

        # Return Phase 1 context
        return self.state.phase1_context

    def run_phase2(self) -> Dict[str, Any]:
        """
        Execute Phase 2: Strategy Analysis.

        Returns:
            Phase 2 results dictionary
        """
        # Step 1: Plan tasks based on Phase 1 results
        logger.info("Planning Phase 2 tasks...")

        phase1_context = self.state.get_phase1_context()
        tasks = self.planner.plan_phase2_tasks(self.config, phase1_context)

        for task in tasks:
            self.state.add_task(task)
            logger.info(f"  - {task.id}: {task.description}")

        # Step 2: Execute tasks
        logger.info(f"\nExecuting {len(tasks)} Phase 2 tasks...")

        completed_task_ids = []

        for task in tasks:
            if self.current_step >= self.max_steps:
                logger.warning(f"Reached max steps ({self.max_steps}) - stopping Phase 2")
                break

            # Check dependencies
            if not self.validator.check_dependencies_met(task, completed_task_ids):
                logger.info(f"Skipping {task.id} - dependencies not met")
                continue

            # Emit task start
            self._emit_progress(
                task_id=task.id,
                task_name=task.description,
                action=f"Starting {task.description}...",
                status=ProgressStatus.IN_PROGRESS,
                level=ProgressLevel.TASK
            )

            # Execute task with Phase 1 context
            self.state.update_task_status(task.id, "in_progress")
            self.executor.reset_loop_detection()

            # Emit skill loading
            skill_name = task.skill.replace('-', ' ').title()
            self._emit_progress(
                task_id=task.id,
                task_name=task.description,
                action=f"Loading {skill_name} skill...",
                status=ProgressStatus.IN_PROGRESS,
                level=ProgressLevel.SKILL
            )

            # Combine Phase 1 and Phase 2 context
            full_context = {**phase1_context, **self.state.phase2_context}

            result = self.executor.execute_task(
                task=task,
                context=full_context,
                config=self.config
            )

            self.current_step += 1

            # Validate result
            is_valid, feedback = self.validator.validate_task_completion(task, result)

            if is_valid:
                # Store result in state
                self._store_phase2_result(task, result)
                self.state.update_task_status(task.id, "completed", result=result)
                completed_task_ids.append(task.id)
                logger.info(f"[OK] {task.id} completed successfully")

                # Emit task completion
                self._emit_progress(
                    task_id=task.id,
                    task_name=task.description,
                    action=f"✓ Completed {task.description}",
                    status=ProgressStatus.COMPLETED,
                    level=ProgressLevel.TASK
                )
            else:
                self.state.update_task_status(task.id, "failed", error=feedback)
                logger.warning(f"[X] {task.id} validation failed: {feedback}")

                # Emit task failure
                self._emit_progress(
                    task_id=task.id,
                    task_name=task.description,
                    action=f"✗ Failed: {feedback}",
                    status=ProgressStatus.FAILED,
                    level=ProgressLevel.TASK,
                    details={'error': feedback}
                )

        # Return Phase 2 context
        return self.state.phase2_context

    def _store_phase1_result(self, task: Task, result: Dict[str, Any]):
        """Store Phase 1 task result in appropriate context bucket."""
        skill = task.skill

        # Map skill to context category
        if 'company-intelligence' in skill:
            self.state.phase1_context['company_intelligence'] = result.get('data', {})
        elif 'business-model-canvas' in skill:
            self.state.phase1_context['business_model_canvas'] = result.get('data', {})
        elif 'value-chain' in skill:
            self.state.phase1_context['value_chain'] = result.get('data', {})
        elif 'org-structure' in skill:
            self.state.phase1_context['org_structure'] = result.get('data', {})
        elif 'market-intelligence' in skill:
            self.state.phase1_context['market_intelligence'] = result.get('data', {})
        elif 'competitor-intelligence' in skill:
            self.state.phase1_context['competitor_intelligence'] = result.get('data', {})
        else:
            # Generic storage
            self.state.phase1_context[skill] = result.get('data', {})

    def _store_phase2_result(self, task: Task, result: Dict[str, Any]):
        """Store Phase 2 task result in appropriate context bucket."""
        skill = task.skill

        # Map skill to context category
        if 'swot' in skill:
            self.state.phase2_context['swot'] = result.get('data', {})
        elif 'porter' in skill:
            self.state.phase2_context['porters_five_forces'] = result.get('data', {})
        elif 'bcg' in skill:
            self.state.phase2_context['bcg_matrix'] = result.get('data', {})
        elif 'blue-ocean' in skill:
            self.state.phase2_context['blue_ocean'] = result.get('data', {})
        elif 'pestel' in skill:
            self.state.phase2_context['pestel'] = result.get('data', {})
        elif 'competitive-strategy' in skill:
            self.state.phase2_context['competitive_strategy'] = result.get('data', {})
        elif 'sales-intelligence' in skill:
            self.state.phase2_context['sales_intelligence'] = result.get('data', {})
        else:
            # Generic storage
            self.state.phase2_context[skill] = result.get('data', {})

    def save_state(self, filepath: str):
        """Save current state for recovery."""
        self.state.save_state(filepath)
        logger.info(f"State saved to {filepath}")

    def load_state(self, filepath: str):
        """Load state from file for recovery."""
        self.state.load_state(filepath)
        logger.info(f"State loaded from {filepath}")
