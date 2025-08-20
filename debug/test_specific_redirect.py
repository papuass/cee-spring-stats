#!/usr/bin/env python3
"""
Debug script to test specific redirect page detection.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.suggested_articles import SuggestedArticlesCollector

def test_specific_redirect():
    """Test the specific redirect page mentioned by the user."""
    
    collector = SuggestedArticlesCollector()
    
    # Test the specific page mentioned
    redirect_page = "Wikimedia CEE Spring 2025/Structure/Ukraine/Tradition & food"
    
    print(f"Testing specific page: {redirect_page}")
    
    # Check if this page is in our current results
    countries = collector.get_suggested_countries()
    
    target_country = "Ukraine/Tradition & food"
    if target_country in countries:
        print(f"❌ PROBLEM: '{target_country}' is in our results but should be filtered as redirect")
    else:
        print(f"✅ GOOD: '{target_country}' is not in our results")
    
    # Make a direct API call to check redirect status
    print(f"\nChecking redirect status directly...")
    
    params = {
        'action': 'query',
        'titles': redirect_page,
        'prop': 'info',
        'format': 'json'
    }
    
    data = collector._make_request(params)
    
    if 'query' in data and 'pages' in data['query']:
        pages = data['query']['pages']
        if isinstance(pages, dict):
            for page_id, page_info in pages.items():
                print(f"Page ID: {page_id}")
                print(f"Title: {page_info.get('title', 'N/A')}")
                if 'redirect' in page_info:
                    print(f"✅ CONFIRMED: This IS a redirect page")
                else:
                    print(f"❌ UNEXPECTED: This is NOT marked as redirect")
                print(f"Full page info: {page_info}")
        elif isinstance(pages, list):
            for page_info in pages:
                print(f"Title: {page_info.get('title', 'N/A')}")
                if 'redirect' in page_info:
                    print(f"✅ CONFIRMED: This IS a redirect page")
                else:
                    print(f"❌ UNEXPECTED: This is NOT marked as redirect")
                print(f"Full page info: {page_info}")
    
    # Test our current API call to see if it's including redirects
    print(f"\nTesting our current API call...")
    
    params = {
        'action': 'query',
        'list': 'allpages',
        'apprefix': 'Wikimedia CEE Spring 2025/Structure/',
        'aplimit': '500',
        'apfilterredir': 'nonredirects',
        'format': 'json'
    }
    
    data = collector._make_request(params)
    
    if 'query' in data and 'allpages' in data['query']:
        ukraine_pages = [page for page in data['query']['allpages'] 
                        if 'Ukraine' in page['title'] and 'Tradition' in page['title']]
        
        print(f"Found {len(ukraine_pages)} Ukraine/Tradition pages:")
        for page in ukraine_pages:
            print(f"  - {page['title']}")
            if 'redirect' in page:
                print(f"    (marked as redirect)")

if __name__ == "__main__":
    test_specific_redirect()