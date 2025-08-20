#!/usr/bin/env python3
"""Test script for dynamic country detection from Meta-Wiki."""

from src.suggested_articles import SuggestedArticlesCollector
from src.config import STRUCTURE_PAGE_PREFIX

def test_dynamic_countries():
    """Test the dynamic country detection."""
    print("="*60)
    print("TESTING DYNAMIC COUNTRY DETECTION")
    print("="*60)
    
    collector = SuggestedArticlesCollector()
    
    # Test getting countries dynamically
    print("Fetching structure pages from Meta-Wiki...")
    countries = collector.get_suggested_countries()
    
    print(f"Found {len(countries)} countries with structure pages:")
    for i, country in enumerate(sorted(countries), 1):
        print(f"  {i:2d}. {country}")
    
    # Test collecting from a few countries
    if countries:
        print(f"\nTesting collection from first 3 countries...")
        test_countries = countries[:3]
        
        total_ids = set()
        for country in test_countries:
            print(f"\nProcessing: {country}")
            page_title = f"{STRUCTURE_PAGE_PREFIX}{country}"
            content = collector.get_page_content(page_title)
            
            if content:
                ids = collector.extract_wikidata_ids_from_content(content)
                total_ids.update(ids)
                print(f"  Found {len(ids)} suggested articles")
            else:
                print(f"  Could not fetch content")
        
        print(f"\nTotal unique IDs from {len(test_countries)} countries: {len(total_ids)}")
    
    return countries

if __name__ == '__main__':
    test_dynamic_countries()