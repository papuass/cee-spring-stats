"""Generator for creating wikitext reports from collected data."""

from typing import List, Dict, Any
from .config import CATEGORY_PREFIX, ALLOWED_CONTEST_COUNTRIES


class ReportGenerator:
    """Generator for creating wikitext reports."""
    
    def __init__(self):
        pass
    
    def generate_wikitext_table(self, articles_data: List[Dict[str, Any]], 
                               title: str = "Konkursā iesniegtie raksti") -> str:
        """
        Generate a wikitext table from articles data.
        
        Args:
            articles_data: List of article data dictionaries
            title: Title for the table section
            
        Returns:
            Formatted wikitext table
        """
        if not articles_data:
            return f"== {title} ==\nNav atrasti raksti ar norādīto veidni.\n"
        
        # Sort articles by participant name, then by article title
        sorted_articles = sorted(articles_data, 
                               key=lambda x: (x.get('participant', '').lower(), 
                                            x.get('title', '').lower()))
        
        # Generate table header
        wikitext = f"== {title} ==\n"
        wikitext += '{| class="sortable wikitable"\n'
        wikitext += '|-\n'
        
        # Table headers
        headers = ['Raksts', 'Dalībnieks', 'Tēma', 'Valsts', 'Lasāmā teksta garums', 'Raksta garums baitos', 'Wikidata ID', 'No ieteikumu saraksta']
        
        wikitext += '! ' + ' !! '.join(headers) + '\n'
        wikitext += '|-\n'
        
        # Generate table rows
        for article in sorted_articles:
            row = self._generate_table_row(article)
            wikitext += row + '\n|-\n'
        
        wikitext += '|}\n'
        
        # Add summary statistics
        wikitext += self._generate_summary_statistics(sorted_articles)
        
        return wikitext
    
    def _generate_table_row(self, article: Dict[str, Any]) -> str:
        """Generate a single table row for an article."""
        title = article.get('title', '')
        participant = article.get('participant', '')
        topics = article.get('topics', [])
        countries = article.get('countries', [])
        readable_length = article.get('readable_length', 0)
        
        # Format article title as link
        article_link = f'[[{title}]]'
        
        # Format participant with user template
        participant_formatted = f'{{{{U|{participant}}}}}' if participant else ''
        
        # Prepare topic column (comma-separated)
        topic_column = ', '.join(topic.strip() for topic in topics if topic.strip())
        
        # Prepare country column using the pre-validated country data
        country_parts = []
        
        # Add valid countries
        valid_countries = article.get('valid_countries', [])
        for country in valid_countries:
            country_parts.append(country)
        
        # Add invalid countries in red
        invalid_countries = article.get('invalid_countries', [])
        for country in invalid_countries:
            country_parts.append(f'<span style="color:red">{country}</span>')
        
        country_column = ', '.join(country_parts)
        
        # Build row data
        # Get actual size in bytes and Wikidata ID from the collected data
        size_bytes = article.get('size_bytes', 0)
        wikidata_id = article.get('wikidata_id', '')
        from_suggested = article.get('from_suggested_list', False)
        
        # Format Wikidata ID as a link if available
        if wikidata_id:
            wikidata_link = f"[[d:{wikidata_id}|{wikidata_id}]]"
        else:
            wikidata_link = ""
        
        # Format suggested list indicator as meta page link or empty
        if from_suggested and 'suggested_country' in article:
            country = article['suggested_country']
            if country:
                suggested_indicator = f"[[m:Wikimedia CEE Spring 2025/Structure/{country}|{country}]]"
            else:
                suggested_indicator = ""
        else:
            suggested_indicator = ""
        
        row_data = [article_link, participant_formatted, topic_column, country_column, str(readable_length), str(size_bytes), wikidata_link, suggested_indicator]
        
        return '| ' + ' || '.join(row_data)
    
    def _generate_summary_statistics(self, articles_data: List[Dict[str, Any]]) -> str:
        """Generate summary statistics section."""
        if not articles_data:
            return ""
        
        total_articles = len(articles_data)
        
        # Count participants
        participants = set()
        for article in articles_data:
            participant = article.get('participant', '').strip()
            if participant:
                participants.add(participant)
        
        total_participants = len(participants)
        
        # Count topics with article counts
        topic_counts = {}
        for article in articles_data:
            for topic in article.get('topics', []):
                if topic.strip():
                    topic_counts[topic.strip()] = topic_counts.get(topic.strip(), 0) + 1
        
        total_topics = len(topic_counts)
        
        # Count countries with article counts
        country_counts = {}
        for article in articles_data:
            for country in article.get('countries', []):
                if country.strip():
                    country_counts[country.strip()] = country_counts.get(country.strip(), 0) + 1
        
        total_countries = len(country_counts)
        
        # Calculate total readable text
        total_readable = sum(article.get('readable_length', 0) for article in articles_data)
        
        # Generate statistics
        stats = f"\n== Statistika ==\n"
        stats += f"* '''Kopējais rakstu skaits:''' {total_articles}\n"
        stats += f"* '''Dalībnieku skaits:''' {total_participants}\n"
        
        # Topics with counts and category links
        stats += f"* '''Dažādu tēmu skaits:''' {total_topics}\n"
        if topic_counts:
            sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
            topic_links = []
            for topic, count in sorted_topics:
                # Create category link for topic (with colon to link to category page)
                topic_lower = topic.lower()
                topic_link = f"[[:Kategorija:{CATEGORY_PREFIX} — {topic_lower}|{topic}]] ({count})"
                topic_links.append(topic_link)
            stats += f"** {', '.join(topic_links)}\n"
        
        # Countries with counts and category links
        stats += f"* '''Dažādu valstu skaits:''' {total_countries}\n"
        if country_counts:
            sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
            country_links = []
            for country, count in sorted_countries:
                # Create category link for country (with colon to link to category page)
                country_link = f"[[:Kategorija:{CATEGORY_PREFIX} — {country}|{country}]] ({count})"
                country_links.append(country_link)
            stats += f"** {', '.join(country_links)}\n"
        
        stats += f"* '''Kopējais lasāmā teksta garums:''' {total_readable:,} rakstzīmes\n"
        
        # Count suggested articles
        suggested_count = sum(1 for article in articles_data if article.get('from_suggested_list', False))
        stats += f"* '''Raksti no ieteikumu saraksta:''' {suggested_count} no {total_articles} ({suggested_count/total_articles*100:.1f}%)\n"
        
        # Top contributors
        participant_stats = {}
        for article in articles_data:
            participant = article.get('participant', '').strip()
            if participant:
                if participant not in participant_stats:
                    participant_stats[participant] = {
                        'articles': 0,
                        'readable_text': 0
                    }
                participant_stats[participant]['articles'] += 1
                participant_stats[participant]['readable_text'] += article.get('readable_length', 0)
        
        # Sort by article count, then by readable text
        top_contributors = sorted(participant_stats.items(), 
                                key=lambda x: (x[1]['articles'], x[1]['readable_text']), 
                                reverse=True)
        
        if top_contributors:
            stats += f"\n=== Aktīvākie dalībnieki ===\n"
            for i, (participant, data) in enumerate(top_contributors, 1):
                stats += f"# {{{{U|{participant}}}}} - {data['articles']} raksti, "
                stats += f"{data['readable_text']:,} rakstzīmes\n"
        
        return stats
    
    def generate_contest_categories_report(self, articles_data: List[Dict[str, Any]]) -> str:
        """Generate a report for different contest categories."""
        if not articles_data:
            return "Nav atrasti raksti ar norādīto veidni.\n"
        
        # Filter articles to only include those eligible for contest
        valid_articles = [article for article in articles_data
                         if article.get('eligible_for_contest', False)]
        
        report = "== Konkursa kategorijas ==\n"
        report += f"''Tikai raksti ar derīgām konkursa valstīm tiek iekļauti šajās kategorijās. "
        report += f"No {len(articles_data)} kopējiem rakstiem, {len(valid_articles)} atbilst kritērijiem.''\n\n"
        
        # 1. Labākais konkursa gaitā tapušais raksts žūrijas vērtējumā
        report += "=== Labākais konkursa gaitā tapušais raksts žūrijas vērtējumā ===\n"
        report += "''(Aizpildīt manuāli)''\n\n"
        
        # 2. Lielākais devums konkursa gaitā - by contribution in bytes
        report += "=== Lielākais devums konkursa gaitā ===\n"
        participant_bytes = {}
        for article in valid_articles:
            participant = article.get('participant', '').strip()
            if participant:
                size_bytes = article.get('size_bytes', 0)
                participant_bytes[participant] = participant_bytes.get(participant, 0) + size_bytes
        
        sorted_by_bytes = sorted(participant_bytes.items(), key=lambda x: x[1], reverse=True)
        for i, (participant, total_bytes) in enumerate(sorted_by_bytes, 1):
            report += f"# {{{{U|{participant}}}}} - {total_bytes:,} baiti\n"
        report += "\n"
        
        # 3. Lielākais devums konkursa gaitā jaunam lietotājam
        report += "=== Lielākais devums konkursa gaitā jaunam lietotājam ===\n"
        report += "''(Aizpildīt manuāli)''\n\n"
        
        # 4. Visvairāk izveidoto rakstu no tēmu sarakstiem
        report += "=== Visvairāk izveidoto rakstu no tēmu sarakstiem ===\n"
        report += "''Minimālais lasāmā teksta apjoms ir 1500 rakstzīmes''\n\n"   
        participant_articles_1500 = {}
        for article in valid_articles:
            participant = article.get('participant', '').strip()
            readable_length = article.get('readable_length', 0)
            from_suggested = article.get('from_suggested_list', False)
            if participant and readable_length >= 1500 and from_suggested:
                participant_articles_1500[participant] = participant_articles_1500.get(participant, 0) + 1
        
        sorted_by_articles_1500 = sorted(participant_articles_1500.items(), key=lambda x: x[1], reverse=True)
        for i, (participant, count) in enumerate(sorted_by_articles_1500, 1):
            report += f"# {{{{U|{participant}}}}} - {count} raksti (no ieteikumu sarakstiem, 1500+ rakstzīmes)\n"
        report += "\n"
        
        # 5. Visvairāk izveidoto rakstu no tēmu sarakstiem jaunam dalībniekam
        report += "=== Visvairāk izveidoto rakstu no tēmu sarakstiem jaunam dalībniekam ===\n"
        report += "''Minimālais lasāmā teksta apjoms ir 1500 rakstzīmes''\n\n"   
        report += "''(Aizpildīt manuāli)''\n\n"
        
        # 6. Visvairāk izveidoto sieviešu biogrāfiju rakstu
        report += "=== Visvairāk izveidoto sieviešu biogrāfiju rakstu ===\n"
        report += "''Minimālais lasāmā teksta apjoms ir 1500 rakstzīmes''\n\n"   
        participant_women_articles = {}
        for article in valid_articles:
            participant = article.get('participant', '').strip()
            readable_length = article.get('readable_length', 0)
            topics = article.get('topics', [])
            
            if participant and readable_length >= 1500 and 'Sievietes' in topics:
                participant_women_articles[participant] = participant_women_articles.get(participant, 0) + 1
        
        sorted_by_women = sorted(participant_women_articles.items(), key=lambda x: x[1], reverse=True)
        for i, (participant, count) in enumerate(sorted_by_women, 1):
            report += f"# {{{{U|{participant}}}}} - {count} raksti\n"
        report += "\n"
        
        # 7. Visvairāk izveidoto cilvēktiesību tēmas rakstu
        report += "=== Visvairāk izveidoto cilvēktiesību tēmas rakstu ===\n"
        report += "''Minimālais lasāmā teksta apjoms ir 1500 rakstzīmes''\n\n"       
        participant_rights_articles = {}
        for article in valid_articles:
            participant = article.get('participant', '').strip()
            readable_length = article.get('readable_length', 0)
            topics = article.get('topics', [])
            
            if participant and readable_length >= 1500 and 'Cilvēktiesības' in topics:
                participant_rights_articles[participant] = participant_rights_articles.get(participant, 0) + 1
        
        sorted_by_rights = sorted(participant_rights_articles.items(), key=lambda x: x[1], reverse=True)
        for i, (participant, count) in enumerate(sorted_by_rights, 1):
            report += f"# {{{{U|{participant}}}}} - {count} raksti\n"
        report += "\n"
        
        return report
    
    def generate_participant_report(self, articles_data: List[Dict[str, Any]]) -> str:
        """Generate a report organized by participants."""
        if not articles_data:
            return "Nav atrasti raksti ar norādīto veidni.\n"
        
        # Group articles by participant
        participants = {}
        for article in articles_data:
            participant = article.get('participant', '').strip()
            if participant:
                if participant not in participants:
                    participants[participant] = []
                participants[participant].append(article)
        
        # Sort participants by name
        sorted_participants = sorted(participants.items())
        
        wikitext = "== Dalībnieku saraksts ==\n"
        
        for participant, articles in sorted_participants:
            wikitext += f"=== {{{{U|{participant}}}}} ===\n"
            wikitext += f"Rakstu skaits: {len(articles)}\n\n"
            
            # Sort articles by title
            sorted_articles = sorted(articles, key=lambda x: x.get('title', ''))
            
            for article in sorted_articles:
                title = article.get('title', '')
                topics = ', '.join(article.get('topics', []))
                countries = ', '.join(article.get('countries', []))
                readable_length = article.get('readable_length', 0)
                
                wikitext += f"* [[{title}]] - "
                if topics:
                    wikitext += f"Tēmas: {topics}; "
                if countries:
                    wikitext += f"Valstis: {countries}; "
                wikitext += f"Lasāmais teksts: {readable_length} rakstzīmes\n"
            
            wikitext += "\n"
        
        return wikitext
    
    def save_report(self, content: str, filename: str) -> bool:
        """Save report content to a file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving report to {filename}: {e}")
            return False