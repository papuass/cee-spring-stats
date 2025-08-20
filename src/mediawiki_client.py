"""MediaWiki API client for fetching Wikipedia data."""

import requests
import time
import json
from typing import Dict, List, Optional, Any
from .config import MEDIAWIKI_API_URL, USER_AGENT, API_RATE_LIMIT


class MediaWikiClient:
    """Client for interacting with MediaWiki API."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self.last_request_time = 0
        
    def _rate_limit(self):
        """Enforce rate limiting between API requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_interval = 1.0 / API_RATE_LIMIT
        
        if time_since_last < min_interval:
            time.sleep(min_interval - time_since_last)
        
        self.last_request_time = time.time()
    
    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the MediaWiki API with rate limiting."""
        self._rate_limit()
        
        # Add common parameters
        params.update({
            'action': params.get('action', 'query'),
            'format': 'json',
            'formatversion': '2'
        })
        
        try:
            response = self.session.get(MEDIAWIKI_API_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return {}
    
    def find_articles_with_template(self, template_name: str, namespace: int = 1) -> List[str]:
        """
        Find all articles that have a specific template on their talk pages.
        
        Args:
            template_name: Name of the template to search for
            namespace: Namespace to search in (1 = talk pages)
            
        Returns:
            List of article titles that have the template
        """
        articles = []
        continue_param = None
        
        while True:
            params = {
                'action': 'query',
                'list': 'embeddedin',
                'eititle': f'Template:{template_name}',
                'einamespace': namespace,
                'eilimit': 500
            }
            
            if continue_param:
                params['eicontinue'] = continue_param
            
            data = self._make_request(params)
            
            if 'query' not in data or 'embeddedin' not in data['query']:
                break
            
            for page in data['query']['embeddedin']:
                # Convert talk page title to article title
                article_title = self._talk_to_article_title(page['title'])
                if article_title:
                    articles.append(article_title)
            
            # Check for continuation
            if 'continue' in data and 'eicontinue' in data['continue']:
                continue_param = data['continue']['eicontinue']
            else:
                break
        
        return articles
    
    def _talk_to_article_title(self, talk_title: str) -> Optional[str]:
        """Convert talk page title to article title."""
        if talk_title.startswith('Diskusija:'):
            return talk_title[10:]  # Remove 'Diskusija:' prefix
        return None
    
    def get_page_content(self, title: str, namespace: int = 0) -> Optional[str]:
        """
        Get the content of a page.
        
        Args:
            title: Page title
            namespace: Namespace (0 = main, 1 = talk)
            
        Returns:
            Page content as string, or None if not found
        """
        if namespace == 1:
            title = f'Diskusija:{title}'
        
        params = {
            'action': 'query',
            'prop': 'revisions',
            'rvprop': 'content',
            'rvslots': 'main',
            'titles': title
        }
        
        data = self._make_request(params)
        
        if 'query' not in data or 'pages' not in data['query']:
            return None
        
        pages = data['query']['pages']
        if not pages:
            return None
        
        page = pages[0]
        if 'missing' in page or 'revisions' not in page:
            return None
        
        revision = page['revisions'][0]
        if 'slots' in revision and 'main' in revision['slots']:
            return revision['slots']['main']['content']
        
        return None
    
    def get_page_info(self, titles: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get basic information about pages including size.
        
        Args:
            titles: List of page titles
            
        Returns:
            Dictionary mapping titles to page info
        """
        if not titles:
            return {}
        
        # Process in batches of 50 (API limit)
        batch_size = 50
        all_info = {}
        
        for i in range(0, len(titles), batch_size):
            batch = titles[i:i + batch_size]
            
            params = {
                'action': 'query',
                'prop': 'info|pageprops',
                'ppprop': 'wikibase_item',
                'titles': '|'.join(batch)
            }
            
            data = self._make_request(params)
            
            if 'query' not in data or 'pages' not in data['query']:
                continue
            
            for page in data['query']['pages']:
                if 'missing' not in page:
                    # Get Wikidata item ID if available
                    wikidata_id = None
                    if 'pageprops' in page and 'wikibase_item' in page['pageprops']:
                        wikidata_id = page['pageprops']['wikibase_item']
                    
                    all_info[page['title']] = {
                        'pageid': page.get('pageid'),
                        'size': page.get('length', 0),  # Use 'length' instead of 'size'
                        'touched': page.get('touched'),
                        'wikidata_id': wikidata_id
                    }
        
        return all_info
    
    def get_page_categories(self, titles: List[str]) -> Dict[str, List[str]]:
        """
        Get categories for pages.
        
        Args:
            titles: List of page titles
            
        Returns:
            Dictionary mapping titles to list of categories
        """
        if not titles:
            return {}
        
        batch_size = 50
        all_categories = {}
        
        for i in range(0, len(titles), batch_size):
            batch = titles[i:i + batch_size]
            
            params = {
                'action': 'query',
                'prop': 'categories',
                'cllimit': 500,
                'titles': '|'.join(batch)
            }
            
            data = self._make_request(params)
            
            if 'query' not in data or 'pages' not in data['query']:
                continue
            
            for page in data['query']['pages']:
                if 'missing' not in page:
                    categories = []
                    if 'categories' in page:
                        categories = [cat['title'] for cat in page['categories']]
                    all_categories[page['title']] = categories
        
        return all_categories