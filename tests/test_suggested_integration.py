#!/usr/bin/env python3
"""Test script for suggested articles integration."""

import os
import sys
from cee_spring_stats import CEESpringStats
from src.config import CONTEST_TEMPLATE

def test_suggested_integration():
    """Test the suggested articles integration with a small sample."""
    print("="*60)
    print("TESTING SUGGESTED ARTICLES INTEGRATION")
    print("="*60)
    
    # Create stats collector
    stats = CEESpringStats()
    
    # Test suggested articles collection
    print("1. Testing suggested articles collection...")
    try:
        suggested_ids = stats.suggested_collector.collect_all_suggested_articles()
        print(f"✅ Found {len(suggested_ids)} suggested Wikidata IDs")
        
        # Show a few examples
        if suggested_ids:
            sample_ids = list(suggested_ids)[:5]
            print(f"   Sample IDs: {', '.join(sample_ids)}")
        
    except Exception as e:
        print(f"❌ Error collecting suggested articles: {e}")
        return False
    
    # Test processing a few articles with suggested check
    print("\n2. Testing article processing with suggested check...")
    try:
        # Get a few article titles
        article_titles = stats.client.find_articles_with_template(CONTEST_TEMPLATE)
        if not article_titles:
            print("❌ No articles found")
            return False
        
        # Process first 3 articles
        test_articles = article_titles[:3]
        print(f"   Processing {len(test_articles)} test articles...")
        
        page_info = stats.client.get_page_info(test_articles)
        
        processed_count = 0
        suggested_count = 0
        
        for title in test_articles:
            try:
                article_data = stats._process_single_article(title, page_info.get(title, {}))
                if article_data:
                    processed_count += 1
                    is_suggested = article_data.get('from_suggested_list', False)
                    if is_suggested:
                        suggested_count += 1
                    
                    print(f"   ✓ {title}: Suggested={is_suggested}, Wikidata={article_data.get('wikidata_id', 'None')}")
                
            except Exception as e:
                print(f"   ❌ Error processing {title}: {e}")
        
        print(f"✅ Processed {processed_count} articles, {suggested_count} from suggested lists")
        
    except Exception as e:
        print(f"❌ Error in article processing test: {e}")
        return False
    
    # Test report generation with suggested column
    print("\n3. Testing report generation with suggested column...")
    try:
        # Create sample data
        sample_data = [
            {
                'title': 'Test Article 1',
                'participant': 'TestUser1',
                'topics': ['Vēsture'],
                'countries': ['Latvija'],
                'readable_length': 1000,
                'size_bytes': 2000,
                'wikidata_id': 'Q123456',
                'from_suggested_list': True
            },
            {
                'title': 'Test Article 2',
                'participant': 'TestUser2',
                'topics': ['Zinātne'],
                'countries': ['Igaunija'],
                'readable_length': 1500,
                'size_bytes': 3000,
                'wikidata_id': 'Q789012',
                'from_suggested_list': False
            }
        ]
        
        # Generate report
        report = stats.reporter.generate_wikitext_table(sample_data, "Test Report")
        
        # Check if suggested column is included
        if "No ieteikumu saraksta" in report and "Jā" in report and "Nē" in report:
            print("✅ Report generation with suggested column works correctly")
            
            # Save test report
            with open('test_suggested_report.txt', 'w', encoding='utf-8') as f:
                f.write(report)
            print("   Test report saved to: test_suggested_report.txt")
        else:
            print("❌ Suggested column not found in report")
            return False
            
    except Exception as e:
        print(f"❌ Error in report generation test: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ ALL SUGGESTED ARTICLES INTEGRATION TESTS PASSED!")
    print("="*60)
    return True

if __name__ == '__main__':
    success = test_suggested_integration()
    sys.exit(0 if success else 1)