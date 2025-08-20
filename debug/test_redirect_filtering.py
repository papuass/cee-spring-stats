#!/usr/bin/env python3
"""
Debug script to test redirect filtering in structure page collection.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.suggested_articles import SuggestedArticlesCollector

def test_redirect_filtering():
    """Test that redirect pages are properly filtered out."""
    
    print("Testing redirect filtering in structure page collection...")
    
    collector = SuggestedArticlesCollector()
    
    # Get structure pages with redirect filtering
    countries = collector.get_suggested_countries()
    
    print(f"\nFound {len(countries)} structure pages (redirects filtered out)")
    print("First 10 countries:")
    for i, country in enumerate(countries[:10]):
        print(f"  {i+1}. {country}")
    
    if len(countries) > 10:
        print(f"  ... and {len(countries) - 10} more")
    
    # Test a few specific pages to make sure they're not redirects
    print("\nTesting a few specific pages for redirect status...")
    
    test_countries = countries[:3] if len(countries) >= 3 else countries
    
    for country in test_countries:
        page_title = f"Wikimedia CEE Spring 2025/Structure/{country}"
        
        # Make a direct API call to check if it's a redirect
        params = {
            'action': 'query',
            'titles': page_title,
            'prop': 'info',
            'format': 'json'
        }
        
        data = collector._make_request(params)
        
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']
            if isinstance(pages, dict):
                for page_id, page_info in pages.items():
                    if 'redirect' in page_info:
                        print(f"  ❌ {country}: IS a redirect (should have been filtered)")
                    else:
                        print(f"  ✅ {country}: Not a redirect")
            elif isinstance(pages, list):
                for page_info in pages:
                    if 'redirect' in page_info:
                        print(f"  ❌ {country}: IS a redirect (should have been filtered)")
                    else:
                        print(f"  ✅ {country}: Not a redirect")
        else:
            print(f"  ⚠️  {country}: Could not check redirect status")

if __name__ == "__main__":
    test_redirect_filtering()