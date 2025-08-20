"""Test script to process only the first 20 articles."""

import sys
from cee_spring_stats import CEESpringStats

class TestCEESpringStats(CEESpringStats):
    """Test version that processes only first 20 articles."""
    
    def _collect_articles_data(self):
        """Collect data for first 20 articles only."""
        # Find all articles with the template
        print(f"Searching for articles with template: {CONTEST_TEMPLATE}")
        article_titles = self.client.find_articles_with_template(CONTEST_TEMPLATE)
        
        if not article_titles:
            print("No articles found with the specified template.")
            return []
        
        # Limit to first 20 articles for testing
        article_titles = article_titles[:20]
        print(f"Testing with first {len(article_titles)} articles.")
        
        # Get page info for all articles
        print("Fetching page information...")
        page_info = self.client.get_page_info(article_titles)
        
        # Process each article
        articles_data = []
        total_articles = len(article_titles)
        
        for i, title in enumerate(article_titles, 1):
            print(f"Processing article {i}/{total_articles}: {title}")
            
            try:
                article_data = self._process_single_article(title, page_info.get(title, {}))
                if article_data:
                    articles_data.append(article_data)
                    print(f"  ✓ Processed: {article_data['participant']} - {len(article_data['topics'])} topics")
                else:
                    print(f"  ✗ Failed to process article")
            except Exception as e:
                print(f"  ✗ Error processing {title}: {e}")
                continue
        
        print(f"Successfully processed {len(articles_data)} articles.")
        return articles_data

def main():
    """Test with 20 articles."""
    print("Testing CEE Spring stats with first 20 articles...")
    
    stats_collector = TestCEESpringStats()
    success = stats_collector.run(use_cache=False, save_cache=False)
    
    if success:
        print("\n🎉 Test completed successfully!")
        print("Check the generated files:")
        print(f"- cee_spring_{CONTEST_YEAR}_results.txt")
        print("- participant_report.txt") 
        print("- contest_categories.txt")
        print("- validation_report.txt")
    else:
        print("❌ Test failed")
        sys.exit(1)

if __name__ == '__main__':
    main()