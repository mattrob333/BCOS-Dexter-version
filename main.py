#!/usr/bin/env python3
"""
Business Context OS - Main Entry Point

Autonomous business research and strategy system for Claude Code.

This is the main entry point that orchestrates:
1. Phase 1: Building comprehensive business context
2. Phase 2: Applying strategic frameworks
3. Generating professional reports

Usage:
    python main.py

Configuration:
    Edit config.yaml to specify target company and research goals
"""

import sys
import yaml
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from core.orchestrator import BusinessContextOrchestrator
from utils.logger import setup_logger, get_default_log_file


def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.yaml
    
    Returns:
        Configuration dictionary
    
    Raises:
        FileNotFoundError: If config.yaml doesn't exist
        yaml.YAMLError: If config.yaml is invalid
    """
    config_path = Path("config.yaml")
    
    if not config_path.exists():
        print("❌ Error: config.yaml not found")
        print("\nPlease create config.yaml with your target company and goals.")
        print("See config.yaml.example for a template.")
        sys.exit(1)
    
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as e:
        print(f"❌ Error: Invalid YAML in config.yaml")
        print(f"Details: {e}")
        sys.exit(1)


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate that required configuration fields are present
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        "company",
        "goals",
        "scope"
    ]
    
    for field in required_fields:
        if field not in config:
            print(f"❌ Error: Missing required field '{field}' in config.yaml")
            return False
    
    if "name" not in config["company"]:
        print("❌ Error: Missing 'company.name' in config.yaml")
        return False
    
    return True


def main():
    """
    Main execution function for Business Context OS
    
    Flow:
        1. Load and validate configuration
        2. Initialize orchestrator
        3. Execute Phase 1: Build business context
        4. Execute Phase 2: Apply strategy frameworks
        5. Generate reports
    """
    
    print("=" * 60)
    print("🚀 Business Context OS")
    print("   Autonomous Business Research & Strategy System")
    print("=" * 60)
    print()
    
    # Load configuration
    config = load_config()
    
    # Validate configuration
    if not validate_config(config):
        sys.exit(1)
    
    company_name = config['company']['name']
    print(f"🎯 Target Company: {company_name}")
    print()

    # Initialize orchestrator
    debug = config.get('advanced', {}).get('debug', False)
    log_file = get_default_log_file() if debug else None

    logger = setup_logger(__name__, debug=debug, log_file=log_file)

    if log_file:
        print(f"📝 Debug logging enabled: {log_file}")
        print()

    print("🔧 Initializing orchestrator...")
    orchestrator = BusinessContextOrchestrator(config)
    print()

    try:
        # Execute the full analysis
        results = orchestrator.run()

        # Check for errors
        if 'error' in results:
            print(f"\n❌ Error during execution: {results['error']}")
            return 1

        # Save results to JSON
        output_dir = Path(f"outputs/{company_name}")
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = output_dir / f"analysis_{timestamp}.json"

        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print()
        print("=" * 60)
        print("✨ Analysis Complete!")
        print("=" * 60)
        print()
        print(f"📁 Results saved to: {results_file}")
        print()

        # Print summary
        summary = results.get('summary', {})
        print("Summary:")
        print(f"  Company: {summary.get('company', company_name)}")
        print(f"  Phase: {summary.get('current_phase', 'complete')}")

        tasks = summary.get('tasks', {})
        if tasks:
            print(f"  Total Tasks: {tasks.get('total', 0)}")
            print(f"  Completed: {tasks.get('completed', 0)}")
            print(f"  Failed: {tasks.get('failed', 0)}")

        print()

        # Save state for potential recovery
        state_file = output_dir / f"state_{timestamp}.json"
        orchestrator.save_state(str(state_file))
        print(f"💾 State saved to: {state_file}")
        print()

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Execution interrupted by user")
        print("State can be recovered from outputs/")
        return 130

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
