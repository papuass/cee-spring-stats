"""Module for collecting suggested article Wikidata IDs from Meta-Wiki pages."""

import requests
import re
from typing import Set, List, Dict
from .config import USER_AGENT, API_RATE_LIMIT, META_WIKI_API_URL, STRUCTURE_PAGE_PREFIX, CONTEST_YEAR
import time


class SuggestedArticlesCollector:
    """Collector for suggested article Wikidata IDs from Meta-Wiki."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self.last_request_time = 0
        self.meta_api_url = META_WIKI_API_URL
    
    def _rate_limit(self):
        """Enforce rate limiting between API requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_interval = 1.0 / API_RATE_LIMIT
        
        if time_since_last < min_interval:
            time.sleep(min_interval - time_since_last)
        
        self.last_request_time = time.time()
    
    def _make_request(self, params: Dict) -> Dict:
        """Make a request to the Meta-Wiki API with rate limiting."""
        self._rate_limit()
        
        # Add common parameters
        params.update({
            'action': params.get('action', 'query'),
            'format': 'json',
            'formatversion': '2'
        })
        
        try:
            response = self.session.get(self.meta_api_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Meta-Wiki API request failed: {e}")
            return {}
    
    def get_page_content(self, title: str) -> str:
        """Get the content of a Meta-Wiki page."""
        params = {
            'action': 'query',
            'prop': 'revisions',
            'rvprop': 'content',
            'rvslots': 'main',
            'titles': title
        }
        
        data = self._make_request(params)
        
        if 'query' not in data or 'pages' not in data['query']:
            return ""
        
        pages = data['query']['pages']
        if not pages:
            return ""
        
        page = pages[0]
        if 'missing' in page or 'revisions' not in page:
            return ""
        
        revision = page['revisions'][0]
        if 'slots' in revision and 'main' in revision['slots']:
            return revision['slots']['main']['content']
        
        return ""
    
    def extract_wikidata_ids_from_content(self, content: str) -> Set[str]:
        """Extract Wikidata IDs from page content."""
        wikidata_ids = set()
        
        # Pattern to match both {{#invoke:WikimediaCEETable|table...}} and {{#invoke:UCDMtable|table...}} with multiline content
        pattern = r'\{\{#invoke:(?:WikimediaCEETable|UCDMtable)\|table[^}]*?\}\}'
        
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            # Remove HTML comments and extract Q-IDs
            # First remove HTML comments like <!--RO--> or <!--MD-->
            clean_match = re.sub(r'<!--[^>]*?-->', '', match)
            
            # Split by | and extract Q-IDs
            parts = clean_match.split('|')
            for part in parts:
                part = part.strip()
                # Remove any trailing }} or other non-alphanumeric characters
                part = re.sub(r'[^Q0-9]', '', part)
                if part.startswith('Q') and len(part) > 1 and part[1:].isdigit():
                    wikidata_ids.add(part)
        
        return wikidata_ids
    
    def get_suggested_countries(self) -> List[str]:
        """Get list of countries that have structure pages from Meta-Wiki API, excluding redirects."""
        params = {
            'action': 'query',
            'list': 'allpages',
            'apprefix': STRUCTURE_PAGE_PREFIX,
            'aplimit': '500',
            'apfilterredir': 'nonredirects',  # Exclude redirect pages
            'format': 'json'
        }
        
        data = self._make_request(params)
        
        if 'query' not in data or 'allpages' not in data['query']:
            print("Could not fetch structure pages from Meta-Wiki")
            return []
        
        countries = []
        redirects_found = 0
        
        for page in data['query']['allpages']:
            title = page['title']
            # Check if this is a redirect (shouldn't happen with apfilterredir, but double-check)
            if 'redirect' in page:
                redirects_found += 1
                continue
                
            # Extract country name from structure page title
            if title.startswith(STRUCTURE_PAGE_PREFIX):
                country = title.replace(STRUCTURE_PAGE_PREFIX, '')
                countries.append(country)
        
        if redirects_found > 0:
            print(f"Filtered out {redirects_found} redirect pages")
        
        print(f"Found {len(countries)} non-redirect structure pages on Meta-Wiki")
        return countries
    
    def collect_all_suggested_wikidata_ids(self) -> Dict[str, Set[str]]:
        """Collect all suggested Wikidata IDs from all country structure pages."""
        countries = self.get_suggested_countries()
        all_suggested_ids = {}
        total_ids = set()
        
        print("Collecting suggested article Wikidata IDs from Meta-Wiki...")
        
        for i, country in enumerate(countries, 1):
            print(f"Processing {i}/{len(countries)}: {country}")
            
            page_title = f"{STRUCTURE_PAGE_PREFIX}{country}"
            content = self.get_page_content(page_title)
            
            if content:
                wikidata_ids = self.extract_wikidata_ids_from_content(content)
                if wikidata_ids:
                    all_suggested_ids[country] = wikidata_ids
                    total_ids.update(wikidata_ids)
                    print(f"  Found {len(wikidata_ids)} Wikidata IDs for {country}")
                else:
                    print(f"  ⚠️  WARNING: No Wikidata IDs found for {country} - page may be empty or have formatting issues")
            else:
                print(f"  Could not fetch content for {country}")
        
        print(f"\nTotal suggested articles collected: {len(total_ids)}")
        print(f"Countries with suggested articles: {len(all_suggested_ids)}")
        
        return all_suggested_ids
    
    def collect_all_suggested_articles(self) -> Set[str]:
        """Collect all suggested Wikidata IDs as a single set."""
        suggested_by_country = self.collect_all_suggested_wikidata_ids()
        all_ids = set()
        for country_ids in suggested_by_country.values():
            all_ids.update(country_ids)
        return all_ids
    
    def save_suggested_ids_to_file(self, suggested_ids: Dict[str, Set[str]], filename: str = "suggested_wikidata_ids.txt"):
        """Save suggested Wikidata IDs to a file for reference."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Suggested Article Wikidata IDs from CEE Spring {CONTEST_YEAR} Structure Pages\n\n")
                
                total_ids = set()
                for country, ids in suggested_ids.items():
                    total_ids.update(ids)
                
                f.write(f"Total suggested articles: {len(total_ids)}\n")
                f.write(f"Countries with suggestions: {len(suggested_ids)}\n\n")
                
                for country, ids in sorted(suggested_ids.items()):
                    f.write(f"== {country} ({len(ids)} articles) ==\n")
                    for wikidata_id in sorted(ids):
                        f.write(f"* {wikidata_id}\n")
                    f.write("\n")
                
                f.write("== All Suggested IDs (for reference) ==\n")
                for wikidata_id in sorted(total_ids):
                    f.write(f"{wikidata_id}\n")
            
            print(f"Suggested Wikidata IDs saved to: {filename}")
            return True
        except Exception as e:
            print(f"Error saving suggested IDs: {e}")
            return False


def main():
    """Test the suggested articles collector."""
    collector = SuggestedArticlesCollector()
    
    # Test with a single country first
    print("Testing with Armenia...")
    from .config import STRUCTURE_PAGE_PREFIX
    content = collector.get_page_content(f"{STRUCTURE_PAGE_PREFIX}Armenia")
    if content:
        ids = collector.extract_wikidata_ids_from_content(content)
        print(f"Found {len(ids)} Wikidata IDs for Armenia: {sorted(list(ids)[:10])}...")
    else:
        print("Could not fetch Armenia page")
    
    # Uncomment to collect all countries (takes longer)
    # all_suggested = collector.collect_all_suggested_wikidata_ids()
    # collector.save_suggested_ids_to_file(all_suggested)


if __name__ == '__main__':
    main()