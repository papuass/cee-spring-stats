"""Parser for extracting data from Wikipedia templates."""

import re
import mwparserfromhell
from typing import Dict, List, Optional, Any
from .config import CONTEST_TEMPLATE


class TemplateParser:
    """Parser for extracting data from Wikipedia templates."""
    
    def __init__(self):
        pass
    
    def parse_cee_spring_template(self, wikitext: str, template_name: str = None) -> Optional[Dict[str, Any]]:
        """
        Parse CEE Spring template from wikitext and extract data.
        
        Args:
            wikitext: The wikitext content containing the template
            template_name: Name of the template to parse (defaults to current contest template)
            
        Returns:
            Dictionary with extracted template data, or None if template not found
        """
        if template_name is None:
            template_name = CONTEST_TEMPLATE
        try:
            parsed = mwparserfromhell.parse(wikitext)
            templates = parsed.filter_templates()
            
            for template in templates:
                # Check if this is the CEE Spring template
                template_title = str(template.name).strip()
                if template_title == template_name:
                    return self._extract_template_data(template)
            
            return None
            
        except Exception as e:
            print(f"Error parsing template: {e}")
            return None
    
    def _extract_template_data(self, template) -> Dict[str, Any]:
        """Extract data from a parsed template object."""
        data = {
            'participant': '',
            'topics': [],
            'countries': []
        }
        
        # Extract parameters from template
        for param in template.params:
            param_name = str(param.name).strip()
            param_value = str(param.value).strip()
            
            if not param_value:
                continue
            
            # Map Latvian field names to English
            if param_name == 'dalībnieks':
                data['participant'] = param_value
            elif param_name.startswith('tēma'):
                # Handle tēma, tēma2, tēma3 and normalize capitalization
                normalized_topic = self._normalize_topic_name(param_value)
                data['topics'].append(normalized_topic)
            elif param_name.startswith('valsts'):
                # Handle valsts, valsts2, valsts3
                data['countries'].append(param_value)
        
        # No limits on topics and countries - parse all
        
        return data
    
    def _normalize_topic_name(self, topic: str) -> str:
        """
        Normalize topic name to ensure it starts with uppercase letter.
        
        Args:
            topic: Original topic name
            
        Returns:
            Normalized topic name with proper capitalization
        """
        if not topic:
            return topic
        
        # Strip whitespace and capitalize first letter
        normalized = topic.strip()
        if normalized:
            # Capitalize first letter while preserving the rest
            normalized = normalized[0].upper() + normalized[1:]
        
        return normalized
    
    def calculate_readable_text_length(self, wikitext: str) -> int:
        """
        Calculate the length of readable text, excluding templates, references, etc.
        
        Args:
            wikitext: The article wikitext content
            
        Returns:
            Length of readable text in characters
        """
        try:
            # Parse the wikitext
            parsed = mwparserfromhell.parse(wikitext)
            
            # Remove templates
            templates_to_remove = list(parsed.filter_templates())
            for template in templates_to_remove:
                try:
                    parsed.remove(template)
                except Exception:
                    # If removal fails, continue with other templates
                    continue
            
            # Convert to text for regex processing
            text = str(parsed)
            
            # Remove gallery tags and their content
            text = re.sub(r'<gallery[^>]*>.*?</gallery>', '', text, flags=re.DOTALL | re.IGNORECASE)
            
            # Remove references - handle self-closing tags first to avoid greedy matching
            # First remove self-closing ref tags like <ref name="..." />
            text = re.sub(r'<ref[^>]*/\s*>', '', text, flags=re.IGNORECASE)
            # Then remove paired ref tags with content like <ref>content</ref>
            text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL | re.IGNORECASE)
            
            # Remove HTML comments
            text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
            
            # Remove other HTML-like tags that might contain non-readable content
            text = re.sub(r'<nowiki[^>]*>.*?</nowiki>', '', text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<pre[^>]*>.*?</pre>', '', text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<code[^>]*>.*?</code>', '', text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<math[^>]*>.*?</math>', '', text, flags=re.DOTALL | re.IGNORECASE)
            
            # Remove categories
            text = re.sub(r'\[\[Category:.*?\]\]', '', text, flags=re.IGNORECASE)
            text = re.sub(r'\[\[Kategorija:.*?\]\]', '', text, flags=re.IGNORECASE)
            
            # Remove file/image links (more comprehensive)
            text = re.sub(r'\[\[File:.*?\]\]', '', text, flags=re.IGNORECASE | re.DOTALL)
            text = re.sub(r'\[\[Attēls:.*?\]\]', '', text, flags=re.IGNORECASE | re.DOTALL)
            text = re.sub(r'\[\[Image:.*?\]\]', '', text, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove external links but keep the text
            text = re.sub(r'\[https?://[^\s\]]+\s+([^\]]+)\]', r'\1', text)
            text = re.sub(r'\[https?://[^\s\]]+\]', '', text)
            
            # Clean up internal links - keep only the display text
            text = re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', r'\2', text)  # [[link|text]] -> text
            text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)  # [[link]] -> link
            
            # Remove wiki markup
            text = re.sub(r"'''([^']+)'''", r'\1', text)  # Bold
            text = re.sub(r"''([^']+)''", r'\1', text)    # Italic
            
            # Remove section headers
            text = re.sub(r'^=+\s*.*?\s*=+\s*$', '', text, flags=re.MULTILINE)
            
            # Remove table markup
            text = re.sub(r'^\{\|.*?\|\}', '', text, flags=re.MULTILINE | re.DOTALL)
            text = re.sub(r'^\|-.*?$', '', text, flags=re.MULTILINE)
            text = re.sub(r'^\|.*?$', '', text, flags=re.MULTILINE)
            text = re.sub(r'^!.*?$', '', text, flags=re.MULTILINE)
            
            # Remove remaining template-like structures that might have been missed
            text = re.sub(r'\{\{[^}]*\}\}', '', text)
            
            # Clean up whitespace
            text = re.sub(r'\n\s*\n', '\n', text)  # Multiple newlines
            text = re.sub(r'[ \t]+', ' ', text)    # Multiple spaces/tabs
            text = text.strip()
            
            return len(text)
            
        except Exception as e:
            print(f"Error calculating readable text length: {e}")
            return 0
    
    def extract_article_data(self, article_title: str, talk_content: str, article_content: str, 
                           page_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extract all relevant data for an article.
        
        Args:
            article_title: Title of the article
            talk_content: Content of the talk page
            article_content: Content of the article
            page_info: Page information from MediaWiki API
            
        Returns:
            Dictionary with all extracted article data
        """
        # Parse template data from talk page
        template_data = self.parse_cee_spring_template(talk_content)
        if not template_data:
            return None
        
        # Calculate readable text length
        readable_length = 0
        if article_content:
            readable_length = self.calculate_readable_text_length(article_content)
        
        # Combine all data
        article_data = {
            'title': article_title,
            'participant': template_data.get('participant', ''),
            'topics': template_data.get('topics', []),
            'countries': template_data.get('countries', []),
            'readable_length': readable_length,
            'size_bytes': page_info.get('size', 0),
            'page_id': page_info.get('pageid', 0),
            'wikidata_id': page_info.get('wikidata_id')
        }
        
        return article_data