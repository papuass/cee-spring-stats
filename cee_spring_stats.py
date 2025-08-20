"""Main script for collecting CEE Spring contest statistics from Wikipedia."""

import json
import os
import sys
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.mediawiki_client import MediaWikiClient
from src.template_parser import TemplateParser
from src.report_generator import ReportGenerator
from src.data_validator import DataValidator
from src.suggested_articles import SuggestedArticlesCollector
from src.config import CONTEST_TEMPLATE, CACHE_FILE, OUTPUT_FILE, ALLOWED_CONTEST_COUNTRIES


class CEESpringStats:
    """Main class for collecting and processing CEE Spring contest statistics."""
    
    def __init__(self):
        self.client = MediaWikiClient()
        self.parser = TemplateParser()
        self.reporter = ReportGenerator()
        self.validator = DataValidator()
        self.suggested_collector = SuggestedArticlesCollector()
        self.cache_file = CACHE_FILE
        self.output_file = OUTPUT_FILE
        self.suggested_ids = set()  # Will store all suggested Wikidata IDs
        self.suggested_by_country = {}  # Will store mapping of Wikidata ID to country
    
    def run(self, use_cache: bool = True, save_cache: bool = True) -> bool:
        """
        Run the complete statistics collection process.
        
        Args:
            use_cache: Whether to use cached data if available
            save_cache: Whether to save data to cache
            
        Returns:
            True if successful, False otherwise
        """
        print(f"Starting CEE Spring {CONTEST_TEMPLATE} statistics collection...")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        # Collect suggested articles from Meta-Wiki
        print("Collecting suggested articles from Meta-Wiki...")
        suggested_by_country = self.suggested_collector.collect_all_suggested_wikidata_ids()
        
        # Build reverse mapping from Wikidata ID to country
        self.suggested_by_country = {}
        self.suggested_ids = set()
        for country, wikidata_ids in suggested_by_country.items():
            for wikidata_id in wikidata_ids:
                self.suggested_by_country[wikidata_id] = country
                self.suggested_ids.add(wikidata_id)
        
        print(f"Found {len(self.suggested_ids)} suggested Wikidata IDs from Meta-Wiki")
        
        # Try to load from cache first
        articles_data = []
        if use_cache and os.path.exists(self.cache_file):
            articles_data = self._load_cache()
            if articles_data:
                print(f"Loaded {len(articles_data)} articles from cache.")
        
        # If no cached data, collect from Wikipedia
        if not articles_data:
            print("Collecting data from Wikipedia...")
            articles_data = self._collect_articles_data()
            
            if not articles_data:
                print("No articles found with the specified template.")
                return False
            
            # Save to cache
            if save_cache:
                self._save_cache(articles_data)
                print(f"Saved {len(articles_data)} articles to cache.")
        
        # Validate and clean data
        print("Validating data...")
        articles_data, errors, warnings = self.validator.validate_articles_data(articles_data)
        
        if errors:
            print("Validation errors found:")
            for error in errors:
                print(f"  ❌ {error}")
            return False
        
        if warnings:
            print("Validation warnings:")
            for warning in warnings[:10]:  # Show first 10 warnings
                print(f"  ⚠️  {warning}")
            if len(warnings) > 10:
                print(f"  ... and {len(warnings) - 10} more warnings")
        
        # Generate reports
        print("Generating reports...")
        success = self._generate_reports(articles_data)
        
        if success:
            print(f"Reports generated successfully!")
            print(f"Main report saved to: {self.output_file}")
            print(f"Participant report saved to: output/participant_report.txt")
            print(f"Contest categories saved to: output/contest_categories.txt")
            print(f"Validation report saved to: output/validation_report.txt")
        else:
            print("Failed to generate reports.")
        
        return success
    
    def _collect_articles_data(self) -> List[Dict[str, Any]]:
        """Collect data for all articles with the CEE Spring template."""
        # Find all articles with the template
        print(f"Searching for articles with template: {CONTEST_TEMPLATE}")
        article_titles = self.client.find_articles_with_template(CONTEST_TEMPLATE)
        
        if not article_titles:
            print("No articles found with the specified template.")
            return []
        
        print(f"Found {len(article_titles)} articles with the template.")
        
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
    
    def _process_single_article(self, title: str, page_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single article and extract all relevant data."""
        # Get talk page content
        talk_content = self.client.get_page_content(title, namespace=1)
        if not talk_content:
            print(f"  Warning: No talk page found for {title}")
            return None
        
        # Get article content for readable text calculation
        article_content = self.client.get_page_content(title, namespace=0)
        if not article_content:
            print(f"  Warning: No article content found for {title}")
            article_content = ""
        
        # Extract article data
        article_data = self.parser.extract_article_data(
            title, talk_content, article_content, page_info
        )
        
        # Check if this article is from suggested list and get country
        if article_data and 'wikidata_id' in article_data:
            wikidata_id = article_data['wikidata_id']
            if wikidata_id in self.suggested_ids:
                article_data['from_suggested_list'] = True
                article_data['suggested_country'] = self.suggested_by_country.get(wikidata_id, '')
            else:
                article_data['from_suggested_list'] = False
                article_data['suggested_country'] = ''
        else:
            article_data['from_suggested_list'] = False
            article_data['suggested_country'] = ''
        
        # Add country validation information
        if article_data:
            countries = article_data.get('countries', [])
            valid_countries = []
            invalid_countries = []
            
            for country in countries:
                country = country.strip()
                if country:
                    if country in ALLOWED_CONTEST_COUNTRIES:
                        valid_countries.append(country)
                    else:
                        invalid_countries.append(country)
            
            article_data['valid_countries'] = valid_countries
            article_data['invalid_countries'] = invalid_countries
            article_data['has_valid_country'] = len(valid_countries) > 0
            article_data['eligible_for_contest'] = len(valid_countries) > 0
        
        return article_data
    
    def _generate_reports(self, articles_data: List[Dict[str, Any]]) -> bool:
        """Generate all reports from the collected data."""
        try:
            # Generate main wikitext table
            main_report = self.reporter.generate_wikitext_table(articles_data)
            success1 = self.reporter.save_report(main_report, self.output_file)
            
            # Generate participant report
            participant_report = self.reporter.generate_participant_report(articles_data)
            success2 = self.reporter.save_report(participant_report, "output/participant_report.txt")
            
            # Generate contest categories report
            categories_report = self.reporter.generate_contest_categories_report(articles_data)
            success3 = self.reporter.save_report(categories_report, "output/contest_categories.txt")
            
            # Generate validation report
            validation_report = self.validator.get_validation_report()
            success4 = self.reporter.save_report(validation_report, "output/validation_report.txt")
            
            return success1 and success2 and success3 and success4
            
        except Exception as e:
            print(f"Error generating reports: {e}")
            return False
    
    def _load_cache(self) -> List[Dict[str, Any]]:
        """Load articles data from cache file."""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('articles', [])
        except Exception as e:
            print(f"Error loading cache: {e}")
            return []
    
    def _save_cache(self, articles_data: List[Dict[str, Any]]) -> bool:
        """Save articles data to cache file."""
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'template': CONTEST_TEMPLATE,
                'articles': articles_data
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving cache: {e}")
            return False
    
    def print_summary(self, articles_data: List[Dict[str, Any]]) -> None:
        """Print a summary of collected data."""
        if not articles_data:
            print("No data to summarize.")
            return
        
        print("\n" + "="*50)
        print("COLLECTION SUMMARY")
        print("="*50)
        
        total_articles = len(articles_data)
        participants = set(article.get('participant', '') for article in articles_data)
        participants.discard('')  # Remove empty participants
        
        topics = set()
        countries = set()
        total_readable = 0
        total_bytes = 0
        
        for article in articles_data:
            for topic in article.get('topics', []):
                if topic.strip():
                    topics.add(topic.strip())
            
            for country in article.get('countries', []):
                if country.strip():
                    countries.add(country.strip())
            
            total_readable += article.get('readable_length', 0)
            total_bytes += article.get('size_bytes', 0)
        
        print(f"Total articles: {total_articles}")
        print(f"Unique participants: {len(participants)}")
        print(f"Unique topics: {len(topics)}")
        print(f"Unique countries: {len(countries)}")
        print(f"Total readable text: {total_readable:,} characters")
        print(f"Total article size: {total_bytes:,} bytes")
        
        # Top participants
        participant_counts = {}
        for article in articles_data:
            participant = article.get('participant', '').strip()
            if participant:
                participant_counts[participant] = participant_counts.get(participant, 0) + 1
        
        if participant_counts:
            print(f"\nTop 5 participants:")
            top_participants = sorted(participant_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for i, (participant, count) in enumerate(top_participants, 1):
                print(f"  {i}. {participant}: {count} articles")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Collect CEE Spring contest statistics from Wikipedia')
    parser.add_argument('--no-cache', action='store_true', help='Do not use cached data')
    parser.add_argument('--no-save-cache', action='store_true', help='Do not save data to cache')
    parser.add_argument('--summary-only', action='store_true', help='Only print summary from cached data')
    
    args = parser.parse_args()
    
    stats_collector = CEESpringStats()
    
    if args.summary_only:
        # Load from cache and print summary
        articles_data = stats_collector._load_cache()
        stats_collector.print_summary(articles_data)
        return
    
    # Run the full collection process
    use_cache = not args.no_cache
    save_cache = not args.no_save_cache
    
    success = stats_collector.run(use_cache=use_cache, save_cache=save_cache)
    
    if success:
        # Print summary
        articles_data = stats_collector._load_cache()
        stats_collector.print_summary(articles_data)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()