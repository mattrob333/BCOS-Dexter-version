"""
Test all API clients (Firecrawl, Exa, Perplexity) to verify they work.

This ensures the Python clients can function in production without MCP.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data_sources.scrapers.firecrawl_client import FirecrawlClient
from data_sources.apis.exa_client import ExaClient
from data_sources.apis.perplexity_client import PerplexityClient
from utils.logger import setup_logger

logger = setup_logger(__name__)


def test_firecrawl():
    """Test Firecrawl Python client."""
    print("\n" + "="*60)
    print("Testing Firecrawl Client")
    print("="*60)

    client = FirecrawlClient()

    if not client.is_available():
        print("[WARN] Firecrawl not available - will use fallback scraping")
        print(f"       API Key set: {'Yes' if os.getenv('FIRECRAWL_API_KEY') else 'No'}")

    # Test scraping
    print("\nTesting: Scrape https://stripe.com")
    result = client.scrape_url("https://stripe.com")

    if result.get('success'):
        content = result.get('content', '')
        print(f"[SUCCESS] Scraped {len(content)} characters")
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Sample: {content[:200]}...")
        return True
    else:
        print(f"[FAIL] Scraping failed: {result.get('error', 'Unknown error')}")
        return False


def test_exa():
    """Test Exa Python client."""
    print("\n" + "="*60)
    print("Testing Exa Client")
    print("="*60)

    client = ExaClient()

    if not client.is_available():
        print("[FAIL] Exa not available")
        print(f"       API Key set: {'Yes' if os.getenv('EXA_API_KEY') else 'No'}")
        return False

    print("[OK] Exa client initialized")

    # Test company search
    print("\nTesting: Search for Stripe company info")
    result = client.search_company_info("Stripe", num_results=3)

    if result.get('success'):
        num_results = result.get('num_results', 0)
        print(f"[SUCCESS] Found {num_results} results")

        results = result.get('results', [])
        for i, r in enumerate(results[:2], 1):
            print(f"\n  Result {i}:")
            print(f"    Title: {r.get('title', 'N/A')[:60]}")
            print(f"    URL: {r.get('url', 'N/A')}")
            print(f"    Text: {r.get('text', 'N/A')[:100]}...")

        return True
    else:
        print(f"[FAIL] Search failed: {result.get('error', 'Unknown error')}")
        return False


def test_perplexity():
    """Test Perplexity Python client."""
    print("\n" + "="*60)
    print("Testing Perplexity Client")
    print("="*60)

    client = PerplexityClient()

    if not client.is_available():
        print("[FAIL] Perplexity not available")
        print(f"       API Key set: {'Yes' if os.getenv('PERPLEXITY_API_KEY') else 'No'}")
        return False

    print("[OK] Perplexity client initialized")

    # Test search
    print("\nTesting: Search for Stripe revenue 2024")
    result = client.search("What is Stripe's annual revenue in 2024?", num_results=3)

    if result.get('success'):
        answer = result.get('answer', '')
        sources = result.get('sources', [])

        print(f"[SUCCESS] Got answer with {len(sources)} sources")
        print(f"\nAnswer: {answer[:300]}...")
        print(f"\nSources ({len(sources)}):")
        for i, source in enumerate(sources[:3], 1):
            print(f"  {i}. {source.get('url', 'N/A')}")

        return True
    else:
        print(f"[FAIL] Search failed: {result.get('error', 'Unknown error')}")
        return False


def main():
    """Run all API client tests."""
    print("\nAPI Client Tests")
    print("="*60)
    print("Testing Python clients for production deployment")
    print("(No MCP dependency - direct API calls)")
    print()

    results = {
        'Firecrawl': test_firecrawl(),
        'Exa': test_exa(),
        'Perplexity': test_perplexity()
    }

    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)

    for name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {name}")

    all_passed = all(results.values())

    if all_passed:
        print("\n[SUCCESS] All API clients working!")
        print("Ready to use Python clients in production.")
    else:
        print("\n[PARTIAL] Some clients failed.")
        print("Check API keys in .env file:")
        print("  - FIRECRAWL_API_KEY")
        print("  - EXA_API_KEY")
        print("  - PERPLEXITY_API_KEY")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
