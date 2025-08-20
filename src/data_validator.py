"""Data validation and duplicate detection utilities."""

from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict


class DataValidator:
    """Validator for article data with duplicate detection and data quality checks."""
    
    def __init__(self):
        self.validation_errors = []
        self.warnings = []
    
    def validate_articles_data(self, articles_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str], List[str]]:
        """
        Validate and clean articles data.
        
        Args:
            articles_data: List of article data dictionaries
            
        Returns:
            Tuple of (cleaned_data, errors, warnings)
        """
        self.validation_errors = []
        self.warnings = []
        
        if not articles_data:
            self.validation_errors.append("No articles data provided")
            return [], self.validation_errors, self.warnings
        
        # Remove duplicates
        cleaned_data = self._remove_duplicates(articles_data)
        
        # Validate each article
        validated_data = []
        for article in cleaned_data:
            if self._validate_single_article(article):
                validated_data.append(self._clean_article_data(article))
        
        # Check for data consistency
        self._check_data_consistency(validated_data)
        
        return validated_data, self.validation_errors, self.warnings
    
    def _remove_duplicates(self, articles_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate articles based on title."""
        seen_titles = set()
        unique_articles = []
        duplicates_found = []
        
        for article in articles_data:
            title = article.get('title', '').strip()
            if not title:
                self.validation_errors.append("Article with empty title found")
                continue
            
            if title in seen_titles:
                duplicates_found.append(title)
                continue
            
            seen_titles.add(title)
            unique_articles.append(article)
        
        if duplicates_found:
            self.warnings.append(f"Removed {len(duplicates_found)} duplicate articles: {', '.join(duplicates_found[:5])}")
            if len(duplicates_found) > 5:
                self.warnings.append(f"... and {len(duplicates_found) - 5} more duplicates")
        
        return unique_articles
    
    def _validate_single_article(self, article: Dict[str, Any]) -> bool:
        """Validate a single article's data."""
        title = article.get('title', '').strip()
        participant = article.get('participant', '').strip()
        
        # Required fields
        if not title:
            self.validation_errors.append("Article with empty title")
            return False
        
        if not participant:
            self.warnings.append(f"Article '{title}' has no participant specified")
        
        # Check data types and ranges
        readable_length = article.get('readable_length', 0)
        size_bytes = article.get('size_bytes', 0)
        
        if not isinstance(readable_length, int) or readable_length < 0:
            self.warnings.append(f"Article '{title}' has invalid readable_length: {readable_length}")
            article['readable_length'] = 0
        
        if not isinstance(size_bytes, int) or size_bytes < 0:
            self.warnings.append(f"Article '{title}' has invalid size_bytes: {size_bytes}")
            article['size_bytes'] = 0
        
        # Check if readable length is reasonable compared to total size
        if readable_length > size_bytes * 2:  # Allow some flexibility
            self.warnings.append(f"Article '{title}' has readable_length ({readable_length}) much larger than size_bytes ({size_bytes})")
        
        # Validate topics and countries
        topics = article.get('topics', [])
        countries = article.get('countries', [])
        
        if not isinstance(topics, list):
            self.warnings.append(f"Article '{title}' has invalid topics format")
            article['topics'] = []
        
        if not isinstance(countries, list):
            self.warnings.append(f"Article '{title}' has invalid countries format")
            article['countries'] = []
        
        # Check for empty topics/countries
        if not topics:
            self.warnings.append(f"Article '{title}' has no topics specified")
        
        if not countries:
            self.warnings.append(f"Article '{title}' has no countries specified")
        
        return True
    
    def _clean_article_data(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and normalize article data."""
        cleaned = article.copy()
        
        # Clean string fields
        cleaned['title'] = cleaned.get('title', '').strip()
        cleaned['participant'] = cleaned.get('participant', '').strip()
        
        # Clean topics and countries lists
        topics = cleaned.get('topics', [])
        cleaned['topics'] = [topic.strip() for topic in topics if topic.strip()]
        
        countries = cleaned.get('countries', [])
        cleaned['countries'] = [country.strip() for country in countries if country.strip()]
        
        # Ensure numeric fields are integers
        cleaned['readable_length'] = max(0, int(cleaned.get('readable_length', 0)))
        cleaned['size_bytes'] = max(0, int(cleaned.get('size_bytes', 0)))
        cleaned['page_id'] = int(cleaned.get('page_id', 0))
        
        return cleaned
    
    def _check_data_consistency(self, articles_data: List[Dict[str, Any]]) -> None:
        """Check for data consistency issues across all articles."""
        if not articles_data:
            return
        
        # Check for participant name variations
        participant_variations = defaultdict(list)
        for article in articles_data:
            participant = article.get('participant', '').strip()
            if participant:
                # Group by lowercase version to find potential variations
                key = participant.lower()
                participant_variations[key].append(participant)
        
        # Report potential participant name variations
        for key, variations in participant_variations.items():
            unique_variations = list(set(variations))
            if len(unique_variations) > 1:
                self.warnings.append(f"Potential participant name variations: {', '.join(unique_variations)}")
        
        # Check for unusual data patterns
        readable_lengths = [article.get('readable_length', 0) for article in articles_data]
        size_bytes = [article.get('size_bytes', 0) for article in articles_data]
        
        if readable_lengths:
            avg_readable = sum(readable_lengths) / len(readable_lengths)
            max_readable = max(readable_lengths)
            
            # Check for unusually long articles
            for article in articles_data:
                length = article.get('readable_length', 0)
                if length > avg_readable * 10:  # More than 10x average
                    self.warnings.append(f"Unusually long article: '{article.get('title')}' ({length} chars)")
        
        if size_bytes:
            avg_size = sum(size_bytes) / len(size_bytes)
            
            # Check for unusually large articles
            for article in articles_data:
                size = article.get('size_bytes', 0)
                if size > avg_size * 10:  # More than 10x average
                    self.warnings.append(f"Unusually large article: '{article.get('title')}' ({size} bytes)")
        
        # Check topic and country distribution
        all_topics = []
        all_countries = []
        
        for article in articles_data:
            all_topics.extend(article.get('topics', []))
            all_countries.extend(article.get('countries', []))
        
        # Count topic frequency
        topic_counts = defaultdict(int)
        for topic in all_topics:
            if topic.strip():
                topic_counts[topic.strip()] += 1
        
        # Count country frequency
        country_counts = defaultdict(int)
        for country in all_countries:
            if country.strip():
                country_counts[country.strip()] += 1
        
        # Report most common topics and countries
        if topic_counts:
            most_common_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            topics_info = ', '.join([f"{topic} ({count})" for topic, count in most_common_topics])
            self.warnings.append(f"Most common topics: {topics_info}")
        
        if country_counts:
            most_common_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            countries_info = ', '.join([f"{country} ({count})" for country, count in most_common_countries])
            self.warnings.append(f"Most common countries: {countries_info}")
    
    def get_validation_report(self) -> str:
        """Generate a validation report."""
        report = []
        
        if self.validation_errors:
            report.append("VALIDATION ERRORS:")
            for error in self.validation_errors:
                report.append(f"  ❌ {error}")
            report.append("")
        
        if self.warnings:
            report.append("WARNINGS:")
            for warning in self.warnings:
                report.append(f"  ⚠️  {warning}")
            report.append("")
        
        if not self.validation_errors and not self.warnings:
            report.append("✅ All data validation checks passed!")
        
        return "\n".join(report)