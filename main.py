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
from pathlib import Path
from typing import Dict, Any

# NOTE: These imports will be created by Claude Code
# from core.orchestrator import BusinessContextOrchestrator
# from core.state_manager import ResearchStateManager
# from utils.logger import setup_logger


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
    
    # TODO: Claude Code will implement these classes
    # Initialize orchestrator
    # logger = setup_logger()
    # orchestrator = BusinessContextOrchestrator(config)
    # state_manager = ResearchStateManager(company_name)
    
    print("=" * 60)
    print("📊 PHASE 1: Building Business Context OS")
    print("=" * 60)
    print()
    print("Tasks:")
    print("  1. Gather company intelligence")
    print("  2. Build Business Model Canvas")
    print("  3. Map Value Chain")
    print("  4. Analyze organizational structure")
    print("  5. Research market landscape")
    print("  6. Profile competitors")
    print()
    
    # TODO: Execute Phase 1
    # context = orchestrator.execute_phase1_foundation(
    #     company_name=company_name,
    #     depth=config['scope']['phase1_depth']
    # )
    # state_manager.save_context(context)
    # print("✅ Phase 1 Complete: Business context established")
    
    print("=" * 60)
    print("🎯 PHASE 2: Executing Strategy Engine")
    print("=" * 60)
    print()
    print("Applying frameworks:")
    frameworks = config['scope'].get('phase2_frameworks', [])
    for framework in frameworks:
        print(f"  - {framework}")
    print()
    
    # TODO: Execute Phase 2
    # strategy = orchestrator.execute_phase2_strategy(
    #     context=context,
    #     goals=config['goals'],
    #     frameworks=config['scope']['phase2_frameworks'],
    #     competitors=config.get('competitors', []),
    #     prospects=config.get('target_prospects', [])
    # )
    # state_manager.save_strategy(strategy)
    # print("✅ Phase 2 Complete: Strategy analysis finished")
    
    print("=" * 60)
    print("📄 Generating Reports")
    print("=" * 60)
    print()
    
    # TODO: Generate reports
    # reports = orchestrator.generate_reports(
    #     context=context,
    #     strategy=strategy,
    #     output_config=config['output']
    # )
    
    print("✨ Analysis Complete!")
    print(f"📁 Reports will be saved to: outputs/{company_name}/")
    print()
    print("TODO: Implementation needed by Claude Code")
    print("This is a starter template - see ARCHITECTURE.md for details")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
