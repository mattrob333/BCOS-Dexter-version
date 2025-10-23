"""
Test script for visualizations.

Run this to test the Business Model Canvas and Value Chain visualizations
with sample data before running a full analysis.
"""

import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from components.visualizations import (
    create_business_model_canvas,
    create_value_chain_diagram
)
from components.data_transformers import (
    transform_bmc_for_visualization,
    transform_value_chain_for_visualization
)


def create_sample_bmc_data():
    """Create sample BMC data for testing."""
    return {
        'key_partners': [
            'Cloud infrastructure providers (AWS, Google Cloud)',
            'Payment processors and financial institutions',
            'Technology integration partners',
            'Strategic consulting firms'
        ],
        'key_activities': [
            'Platform development and maintenance',
            'Customer onboarding and support',
            'Security and compliance management',
            'Continuous product innovation'
        ],
        'key_resources': [
            'Proprietary technology platform',
            'Engineering and data science team',
            'Brand reputation and market presence',
            'Customer data and insights'
        ],
        'value_propositions': [
            'Enterprise: Scalable payment infrastructure with advanced features',
            'SMBs: Easy-to-integrate payment solution with transparent pricing',
            'Developers: Well-documented APIs and robust developer tools'
        ],
        'customer_relationships': [
            'Dedicated account management for enterprise clients',
            'Self-service platform with comprehensive documentation',
            'Community forums and developer support',
            '24/7 technical support'
        ],
        'channels': [
            'Direct sales team for enterprise',
            'Online platform and self-service signup',
            'Partner network and integrations',
            'Developer community and events'
        ],
        'customer_segments': [
            'E-commerce businesses',
            'SaaS companies',
            'Marketplaces and platforms',
            'Enterprise retailers'
        ],
        'cost_structure': [
            'Technology infrastructure and hosting',
            'Engineering and product development',
            'Sales and marketing',
            'Compliance and regulatory',
            'Customer support operations'
        ],
        'revenue_streams': [
            'Transaction fees (percentage of payment volume)',
            'Subscription fees for premium features',
            'Professional services and integration support',
            'Value-added services (fraud detection, analytics)'
        ]
    }


def create_sample_value_chain_data():
    """Create sample Value Chain data for testing."""
    return {
        'primary_activities': {
            'inbound_logistics': {
                'description': 'Data ingestion from merchants and financial institutions',
                'key_elements': [
                    'Real-time payment data processing',
                    'Secure API connections',
                    'Data validation and quality checks'
                ],
                'competitive_advantage': 'Industry-leading data processing speed and accuracy'
            },
            'operations': {
                'description': 'Payment processing and transaction management',
                'key_elements': [
                    'Multi-currency payment processing',
                    'Fraud detection algorithms',
                    'Automated reconciliation'
                ],
                'competitive_advantage': '99.99% uptime with advanced fraud prevention'
            },
            'outbound_logistics': {
                'description': 'Distribution of funds and settlement',
                'key_elements': [
                    'Fast settlement times',
                    'Multi-channel payout options',
                    'Automated reporting'
                ],
                'competitive_advantage': 'Fastest settlement in the industry (1-2 days)'
            },
            'marketing_sales': {
                'description': 'Customer acquisition and relationship management',
                'key_elements': [
                    'Developer-first marketing approach',
                    'Enterprise sales team',
                    'Partner ecosystem development'
                ],
                'competitive_advantage': 'Strong developer community and brand recognition'
            },
            'service': {
                'description': 'Customer support and success',
                'key_elements': [
                    '24/7 technical support',
                    'Dedicated account management',
                    'Comprehensive documentation'
                ],
                'competitive_advantage': 'Industry-leading customer satisfaction scores'
            }
        },
        'support_activities': {
            'firm_infrastructure': {
                'description': 'Corporate governance and strategic planning',
                'key_elements': [
                    'Strong executive leadership',
                    'Global compliance framework',
                    'Strategic partnerships'
                ],
                'competitive_advantage': 'Proven track record of sustainable growth'
            },
            'hrm': {
                'description': 'Talent acquisition and development',
                'key_elements': [
                    'Top-tier engineering talent',
                    'Continuous learning programs',
                    'Strong company culture'
                ],
                'competitive_advantage': 'Ability to attract and retain top tech talent'
            },
            'technology_development': {
                'description': 'Innovation and R&D',
                'key_elements': [
                    'Advanced machine learning capabilities',
                    'Continuous platform improvement',
                    'Emerging technology exploration'
                ],
                'competitive_advantage': 'Cutting-edge payment technology and innovation'
            },
            'procurement': {
                'description': 'Vendor and partner management',
                'key_elements': [
                    'Strategic vendor relationships',
                    'Infrastructure optimization',
                    'Cost management'
                ],
                'competitive_advantage': 'Economies of scale in infrastructure costs'
            }
        },
        'summary': 'Integrated value chain focused on developer experience and reliability'
    }


def test_bmc_visualization():
    """Test Business Model Canvas visualization."""
    print("Testing Business Model Canvas visualization...")

    sample_data = create_sample_bmc_data()

    try:
        fig = create_business_model_canvas(sample_data, title="Test Company - Business Model Canvas")
        print("✓ BMC visualization created successfully")
        print(f"  - Figure has {len(fig.data)} traces")
        print(f"  - Figure dimensions: {fig.layout.width}x{fig.layout.height}")

        # Try to save
        fig.write_html("test_bmc.html")
        print("✓ BMC saved to test_bmc.html")

        return True

    except Exception as e:
        print(f"✗ BMC visualization failed: {str(e)}")
        return False


def test_value_chain_visualization():
    """Test Value Chain visualization."""
    print("\nTesting Value Chain visualization...")

    sample_data = create_sample_value_chain_data()

    try:
        fig = create_value_chain_diagram(sample_data, title="Test Company - Value Chain")
        print("✓ Value Chain visualization created successfully")
        print(f"  - Figure has {len(fig.data)} traces")
        print(f"  - Figure dimensions: {fig.layout.width}x{fig.layout.height}")

        # Try to save
        fig.write_html("test_value_chain.html")
        print("✓ Value Chain saved to test_value_chain.html")

        return True

    except Exception as e:
        print(f"✗ Value Chain visualization failed: {str(e)}")
        return False


def test_data_transformers():
    """Test data transformation functions."""
    print("\nTesting data transformers...")

    # Mock Phase 1 results
    mock_phase1 = {
        'business_model_canvas': create_sample_bmc_data(),
        'value_chain': {
            'findings': create_sample_value_chain_data()
        }
    }

    try:
        # Test BMC transformer
        bmc_viz = transform_bmc_for_visualization(mock_phase1)
        print("✓ BMC data transformer works")
        print(f"  - Transformed {len(bmc_viz)} sections")

        # Test Value Chain transformer
        vc_viz = transform_value_chain_for_visualization(mock_phase1)
        print("✓ Value Chain data transformer works")
        print(f"  - Primary activities: {len(vc_viz.get('primary_activities', {}))}")
        print(f"  - Support activities: {len(vc_viz.get('support_activities', {}))}")

        return True

    except Exception as e:
        print(f"✗ Data transformers failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("BCOS Visualization Tests")
    print("=" * 60)

    results = []

    # Test data transformers
    results.append(("Data Transformers", test_data_transformers()))

    # Test BMC
    results.append(("Business Model Canvas", test_bmc_visualization()))

    # Test Value Chain
    results.append(("Value Chain", test_value_chain_visualization()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n✓ All tests passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the Streamlit app: streamlit run app.py")
        print("3. Complete an analysis to see the visualizations in action")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")

    return all_passed


if __name__ == "__main__":
    main()
