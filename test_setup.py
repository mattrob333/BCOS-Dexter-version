#!/usr/bin/env python3
"""
Quick setup test for BCOS.
Verifies core components are working without running full analysis.
"""

import sys
from pathlib import Path

print("=" * 60)
print("BCOS Setup Test")
print("=" * 60)
print()

# Test 1: Python version
print("[OK] Python version:", sys.version.split()[0])

# Test 2: Import core modules
print("\nTesting core imports...")
try:
    from core.orchestrator import BusinessContextOrchestrator
    print("  [OK] Orchestrator")
except Exception as e:
    print(f"  [X] Orchestrator: {e}")

try:
    from core.planner import Planner
    print("  [OK] Planner")
except Exception as e:
    print(f"  [X] Planner: {e}")

try:
    from core.executor import Executor
    print("  [OK] Executor")
except Exception as e:
    print(f"  [X] Executor: {e}")

try:
    from core.validator import Validator
    print("  [OK] Validator")
except Exception as e:
    print(f"  [X] Validator: {e}")

try:
    from core.state_manager import StateManager
    print("  [OK] State Manager")
except Exception as e:
    print(f"  [X] State Manager: {e}")

# Test 3: Check dependencies
print("\nTesting key dependencies...")
deps_ok = True

try:
    import anthropic
    print(f"  [OK] anthropic ({anthropic.__version__})")
except Exception as e:
    print(f"  [X] anthropic: {e}")
    deps_ok = False

try:
    import langchain
    print(f"  [OK] langchain")
except Exception as e:
    print(f"  [X] langchain: {e}")
    deps_ok = False

try:
    from exa_py import Exa
    print(f"  [OK] exa-py")
except Exception as e:
    print(f"  [X] exa-py: {e}")

try:
    import yaml
    print(f"  [OK] yaml")
except Exception as e:
    print(f"  [X] yaml: {e}")
    deps_ok = False

# Test 4: Check environment
print("\nChecking environment...")
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('ANTHROPIC_API_KEY')
if api_key and api_key != 'your-anthropic-api-key-here':
    print(f"  [OK] ANTHROPIC_API_KEY configured ({api_key[:8]}...)")
else:
    print(f"  [!] ANTHROPIC_API_KEY not set - add it to .env file")
    deps_ok = False

# Test 5: Check config
print("\nChecking configuration...")
config_file = Path("config.yaml")
if config_file.exists():
    print(f"  [OK] config.yaml exists")
    try:
        with open(config_file) as f:
            import yaml
            config = yaml.safe_load(f)
            print(f"  [OK] Target company: {config.get('company', {}).get('name', 'Not set')}")
    except Exception as e:
        print(f"  [X] Error reading config.yaml: {e}")
else:
    print(f"  [X] config.yaml not found")

# Test 6: Check skills
print("\nChecking skills...")
skills_dir = Path("skills")
if skills_dir.exists():
    phase1_skills = list(Path("skills/phase1_foundation").glob("*/"))
    phase2_skills = list(Path("skills/phase2_strategy").glob("*/"))
    print(f"  [OK] Phase 1 skills: {len(phase1_skills)} found")
    print(f"  [OK] Phase 2 skills: {len(phase2_skills)} found")
else:
    print(f"  [X] skills/ directory not found")

# Summary
print("\n" + "=" * 60)
if deps_ok:
    print("[OK] Core setup looks good!")
    print()
    print("Next steps:")
    print("1. Add your ANTHROPIC_API_KEY to .env file")
    print("2. Edit config.yaml with your target company")
    print("3. Run: python main.py")
else:
    print("[WARNING] Some issues detected - see above")
    print()
    print("To fix:")
    print("1. Add ANTHROPIC_API_KEY to .env file")
    print("2. Ensure all dependencies installed: pip install -r requirements.txt")
print("=" * 60)
