"""Test script to verify the CEE Spring statistics tool functionality."""

import sys
from mediawiki_client import MediaWikiClient
from template_parser import TemplateParser
from config import CONTEST_TEMPLATE


def test_api_connection():
    """Test basic API connection to Latvian Wikipedia."""
    print("Testing API connection to Latvian Wikipedia...")
    
    client = MediaWikiClient()
    
    # Test a simple API call
    params = {
        'action': 'query',
        'meta': 'siteinfo',
        'siprop': 'general'
    }
    
    result = client._make_request(params)
    
    if 'query' in result and 'general' in result['query']:
        site_name = result['query']['general'].get('sitename', 'Unknown')
        print(f"✅ Successfully connected to: {site_name}")
        return True
    else:
        print("❌ Failed to connect to API")
        return False


def test_template_search():
    """Test searching for articles with the CEE Spring template."""
    print(f"\nTesting template search for: {CONTEST_TEMPLATE}")
    
    client = MediaWikiClient()
    
    # Search for articles with the template
    articles = client.find_articles_with_template(CONTEST_TEMPLATE)
    
    print(f"Found {len(articles)} articles with the template")
    
    if articles:
        print("Sample articles found:")
        for i, article in enumerate(articles[:5], 1):
            print(f"  {i}. {article}")
        
        if len(articles) > 5:
            print(f"  ... and {len(articles) - 5} more articles")
        
        return True, articles[:3]  # Return first 3 for further testing
    else:
        print("No articles found with the specified template")
        return False, []


def test_template_parsing():
    """Test parsing template data from a sample."""
    print("\nTesting template parsing...")
    
    # Sample template content
    sample_template = f"""
{{{{{CONTEST_TEMPLATE}
|dalībnieks = Votre Provocateur
|tēma     = Sabiedrība
|valsts     = Ukraina
|valsts2    = Rumānija un Moldova
|valsts3    = Bulgārija
}}}}
"""
    
    parser = TemplateParser()
    result = parser.parse_cee_spring_template(sample_template)
    
    if result:
        print("✅ Template parsing successful:")
        print(f"  Participant: {result.get('participant')}")
        print(f"  Topics: {result.get('topics')}")
        print(f"  Countries: {result.get('countries')}")
        return True
    else:
        print("❌ Template parsing failed")
        return False


def test_single_article(article_title):
    """Test processing a single article."""
    print(f"\nTesting single article processing: {article_title}")
    
    client = MediaWikiClient()
    parser = TemplateParser()
    
    try:
        # Get talk page content
        talk_content = client.get_page_content(article_title, namespace=1)
        if not talk_content:
            print(f"❌ No talk page found for {article_title}")
            return False
        
        # Get page info
        page_info = client.get_page_info([article_title])
        article_info = page_info.get(article_title, {})
        
        # Get article content
        article_content = client.get_page_content(article_title, namespace=0)
        
        # Extract data
        article_data = parser.extract_article_data(
            article_title, talk_content, article_content or "", article_info
        )
        
        if article_data:
            print("✅ Article processing successful:")
            print(f"  Title: {article_data.get('title')}")
            print(f"  Participant: {article_data.get('participant')}")
            print(f"  Topics: {article_data.get('topics')}")
            print(f"  Countries: {article_data.get('countries')}")
            print(f"  Size (bytes): {article_data.get('size_bytes')}")
            print(f"  Readable length: {article_data.get('readable_length')}")
            return True
        else:
            print("❌ Failed to extract article data")
            return False
            
    except Exception as e:
        print(f"❌ Error processing article: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("CEE SPRING STATISTICS TOOL - TEST SUITE")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: API Connection
    total_tests += 1
    if test_api_connection():
        tests_passed += 1
    
    # Test 2: Template Search
    total_tests += 1
    search_success, sample_articles = test_template_search()
    if search_success:
        tests_passed += 1
    
    # Test 3: Template Parsing
    total_tests += 1
    if test_template_parsing():
        tests_passed += 1
    
    # Test 4: Single Article Processing (if we have sample articles)
    if sample_articles:
        total_tests += 1
        if test_single_article(sample_articles[0]):
            tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The tool is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)