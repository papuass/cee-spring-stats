#!/usr/bin/env python3
"""
Debug script to test MediaWiki API page size collection.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.mediawiki_client import MediaWikiClient

def test_page_size():
    """Test page size collection for a few articles."""
    client = MediaWikiClient()
    
    # Test with a few known articles
    test_titles = [
        "Džagatajs",
        "Anatolijs Šundels", 
        "GAZ-51"
    ]
    
    print("Testing page info collection...")
    page_info = client.get_page_info(test_titles)
    
    for title in test_titles:
        if title in page_info:
            info = page_info[title]
            print(f"\n{title}:")
            print(f"  Page ID: {info.get('pageid')}")
            print(f"  Size: {info.get('size')} bytes")
            print(f"  Touched: {info.get('touched')}")
            print(f"  Wikidata ID: {info.get('wikidata_id')}")
        else:
            print(f"\n{title}: Not found in results")
    
    # Also test direct API call to see raw response
    print("\n" + "="*50)
    print("Testing direct API call...")
    
    params = {
        'action': 'query',
        'prop': 'info|pageprops',
        'ppprop': 'wikibase_item',
        'titles': '|'.join(test_titles[:2])  # Test with first 2 titles
    }
    
    raw_data = client._make_request(params)
    print("Raw API response:")
    
    if 'query' in raw_data and 'pages' in raw_data['query']:
        for page in raw_data['query']['pages']:
            print(f"\nPage data: {page}")
    else:
        print("No pages found in response")
        print(f"Full response: {raw_data}")

if __name__ == "__main__":
    test_page_size()