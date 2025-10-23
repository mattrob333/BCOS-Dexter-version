"""
Quick test of multi-source verification system.

Tests the new Company Intelligence skill with Truth Engine.
"""

import sys
from pathlib import Path
import yaml
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.state_manager import Task
from skills.phase1_foundation.company_intelligence import execute as company_intel_execute
from utils.logger import setup_logger

logger = setup_logger(__name__)


def test_company_intelligence():
    """Test Company Intelligence with multi-source verification."""

    print("\n" + "="*60)
    print("[TEST] Multi-Source Company Intelligence")
    print("="*60 + "\n")

    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    company = config.get('company', {})
    company_name = company.get('name', 'Unknown')

    print(f"Target Company: {company_name}")
    print(f"Website: {company.get('website', 'N/A')}")
    print(f"Industry: {company.get('industry', 'N/A')}")
    print()

    # Create mock task
    task = Task(
        id="test_task_1",
        description="Gather comprehensive company intelligence",
        phase="phase1",
        skill="company-intelligence"
    )

    # Create context
    context = {
        'company': company
    }

    print("Executing Company Intelligence skill...")
    print("   - Scraping website with Firecrawl")
    print("   - Deep research with Exa")
    print("   - Verification with Perplexity")
    print("   - Cross-referencing with Truth Engine")
    print()

    try:
        # Execute skill
        result = company_intel_execute(task, context, config)

        if result.get('success'):
            print("[SUCCESS] Skill execution successful!\n")

            # Extract verified dataset
            verified_dataset = result.get('verified_dataset', {})

            # Display summary
            print("VERIFICATION SUMMARY")
            print("-" * 60)
            print(f"Entity: {verified_dataset.get('entity_name', 'Unknown')}")
            print(f"Overall Confidence: {verified_dataset.get('overall_confidence', 0):.1%}")
            print(f"Total Sources Used: {verified_dataset.get('total_sources', 0)}")
            print(f"[+] Verified Facts: {verified_dataset.get('verified_count', 0)}")
            print(f"[!] Unverified Facts: {verified_dataset.get('unverified_count', 0)}")
            print(f"[*] Conflicts Detected: {verified_dataset.get('conflict_count', 0)}")
            print()

            # Display sample facts
            facts = verified_dataset.get('facts', [])

            if facts:
                print("SAMPLE VERIFIED FACTS")
                print("-" * 60)

                for i, fact in enumerate(facts[:5], 1):  # Show first 5
                    print(f"\n{i}. {fact.get('claim', 'Unknown Claim')}")
                    print(f"   Value: {fact.get('value', 'N/A')}")
                    print(f"   Confidence: {fact.get('confidence', 0):.1%} ({fact.get('confidence_level', 'unknown')})")
                    print(f"   Verified: {'[YES]' if fact.get('verified') else '[NO]'}")

                    # Show sources
                    sources = fact.get('sources', [])
                    if sources:
                        print(f"   Sources ({len(sources)}):")
                        for source in sources[:2]:  # Show first 2 sources
                            source_type = source.get('source_type', 'unknown')
                            source_name = source.get('source_name', 'Unknown')
                            reliability = source.get('reliability_score', 0)
                            print(f"      - {source_name} ({source_type}, reliability: {reliability:.0%})")

                    # Show conflicts if any
                    conflicts = fact.get('conflicts', [])
                    if conflicts:
                        print(f"   [WARNING] {len(conflicts)} conflict(s) detected")

                if len(facts) > 5:
                    print(f"\n   ... and {len(facts) - 5} more facts")

            print("\n" + "="*60)
            print("[PASS] TEST PASSED - Multi-source verification working!")
            print("="*60 + "\n")

            # Show verification method
            print("Verification Method:")
            print(f"   {result.get('verification_method', 'unknown')}")
            print(f"   Sources used: {result.get('sources_used', 0)}")
            print()

            return True

        else:
            print("[FAIL] Skill execution failed")
            print(f"Error: {result.get('error', 'Unknown error')}")
            return False

    except Exception as e:
        print(f"[FAIL] TEST FAILED with exception:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\nStarting Multi-Source Verification Test\n")

    success = test_company_intelligence()

    if success:
        print("\n[PASS] All tests passed! Multi-source system is operational.\n")
        print("Next steps:")
        print("  1. Review the verification results above")
        print("  2. Check confidence scores and source attribution")
        print("  3. Continue with UI/Report updates")
        print()
    else:
        print("\n[FAIL] Tests failed. Review errors above.\n")

    sys.exit(0 if success else 1)
