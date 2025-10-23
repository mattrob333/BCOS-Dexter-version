"""Quick test of company_intelligence skill."""
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from skills.phase1_foundation.company_intelligence import execute
from core.state_manager import Task
import yaml

# Load config
with open('config.yaml') as f:
    config = yaml.safe_load(f)

# Create test task
task = Task(
    id="test_task",
    description="Test company intelligence gathering",
    phase="phase1",
    skill="company_intelligence"
)

# Execute
print("Testing company_intelligence skill...")
print(f"Company: {config['company']['name']}")
print("=" * 60)

result = execute(task, context={}, config=config)

# Print result
if result.get('success'):
    dataset = result.get('verified_dataset', {})
    facts = dataset.get('facts', [])

    print(f"\nFound {len(facts)} facts:")
    print("=" * 60)

    # Find key_facts
    for fact in facts:
        if fact['claim'] == 'key_facts':
            print("\nKey Facts:")
            print(json.dumps(fact['value'], indent=2))
            print(f"\nConfidence: {fact['confidence']:.2f}")
            print(f"Sources: {len(fact['sources'])}")
            break
else:
    print(f"ERROR: {result.get('error')}")
