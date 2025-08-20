"""Debug script to test page size collection."""

from mediawiki_client import MediaWikiClient

def test_page_size():
    """Test page size collection for a few articles."""
    client = MediaWikiClient()
    
    # Test with a few known articles
    test_articles = ["Džagatajs", "Persiešu alfabēts", "Armēnijas revolūcija (2018)"]
    
    print("Testing page size collection...")
    
    # Get page info
    page_info = client.get_page_info(test_articles)
    
    print(f"Found info for {len(page_info)} articles:")
    for title, info in page_info.items():
        print(f"  {title}: {info}")
    
    # Test individual API call
    print("\nTesting direct API call...")
    params = {
        'action': 'query',
        'prop': 'info',
        'inprop': 'size',
        'titles': 'Džagatajs'
    }
    
    result = client._make_request(params)
    print(f"Direct API result: {result}")

if __name__ == '__main__':
    test_page_size()