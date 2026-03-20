# CEE Spring Statistics Tool

A comprehensive tool for collecting and analyzing statistics from Wikipedia articles submitted to the CEE Spring contest. This tool automatically gathers data from articles tagged with the `{{CEE Spring 2026}}` template and generates comprehensive reports in wikitext format.

## 🏗️ Project Structure

```
cee-spring-stats/
├── 📁 src/                     # Source code modules
│   ├── __init__.py
│   ├── config.py               # Configuration settings
│   ├── mediawiki_client.py     # MediaWiki API client
│   ├── template_parser.py      # Template parsing logic
│   ├── report_generator.py     # Report generation
│   ├── data_validator.py       # Data validation
│   └── suggested_articles.py   # Meta-Wiki suggested articles collector
├── 📁 tests/                   # Test scripts
│   ├── test_tool.py           # Main test suite
│   ├── test_suggested_integration.py  # Suggested articles tests
│   ├── test_multiple_topics.py       # Multiple topics tests
│   ├── test_20_articles.py           # Limited article tests
│   └── test_topic_normalization.py   # Topic normalization tests
├── 📁 output/                  # Generated reports and results (auto-created)
│   ├── cee_spring_2026_results.txt   # Main wikitext report
│   ├── participant_report.txt        # Participant breakdown
│   ├── contest_categories.txt        # Contest categories
│   └── validation_report.txt         # Data validation report
├── 📁 cache/                   # Cached data files (auto-created)
│   └── cee_spring_2026_cache.json    # Article data cache
├── 📁 debug/                   # Debug and analysis scripts
├── 📁 docs/                    # Documentation
│   └── USAGE_EXAMPLES.md      # Usage examples and guides
├── cee_spring_stats.py        # Main entry point script
├── pyproject.toml             # Project dependencies (managed with uv)
└── .env.example              # Environment variables template
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the tool:**
   ```bash
   python cee_spring_stats.py
   ```

3. **View results:**
   - Main report: `output/cee_spring_2026_results.txt`
   - Participant breakdown: `output/participant_report.txt`
   - Contest categories: `output/contest_categories.txt`

## ✨ Key Features

### 📊 **Comprehensive Data Collection**
- Automatically finds all articles with CEE Spring 2025 template
- Collects article metadata (size, readable text length, Wikidata IDs)
- Extracts participant information and topics
- Supports multiple topics and countries per article

### 🌐 **Suggested Articles Integration**
- Automatically collects suggested article lists from Meta-Wiki
- Identifies which contest articles were created from suggestions
- Provides statistics on suggestion effectiveness
- Handles duplicate detection across 29 countries

### 📝 **Rich Report Generation**
- **Main Report**: Sortable wikitext table for Wikipedia publication
- **Participant Report**: Individual contributor breakdowns
- **Contest Categories**: Award category analysis
- **Validation Report**: Data quality insights

### 🔍 **Data Quality & Validation**
- Duplicate article detection
- Data consistency checks
- Topic and country normalization
- Comprehensive error reporting

### ⚡ **Performance & Reliability**
- Intelligent caching system
- Rate-limited API requests (1 req/sec)
- Robust error handling
- Progress tracking and logging

## 📋 Usage Examples

### Basic Collection
```bash
python cee_spring_stats.py
```

### Command Line Options
```bash
python cee_spring_stats.py --help
```

Available options:
- `--no-cache`: Don't use cached data, collect fresh from Wikipedia
- `--no-save-cache`: Don't save collected data to cache
- `--summary-only`: Only print summary from cached data (no collection)

### Testing the Tool

Before running the full collection, test the tool:

```bash
python tests/test_tool.py
```

This will verify:
- API connection to Latvian Wikipedia
- Template search functionality
- Data parsing capabilities
- Single article processing

## 📊 Sample Output

The tool generates comprehensive reports including:

- **523 articles** from **24 participants**
- **31 unique topics** across **50 countries**
- **782,628 characters** of readable text
- **29.8%** of articles from suggested lists

## 📄 Output Files

The tool generates several output files:

### 1. Main Results (`cee_spring_2026_results.txt`)

A wikitext table ready for publishing on Wikipedia:

```wikitext
== Konkursā iesniegtie raksti ==
{| class="sortable wikitable"
|-
! Raksts !! Dalībnieks !! Tēma !! Valsts !! Lasāmā teksta garums !! Raksta garums baitos !! Wikidata ID !! No ieteikumu saraksta
|-
| [[Article Title]] || {{U|Username}} || Topic1, Topic2 || Country1, Country2 || 1234 || 3894 || [[d:Q123456|Q123456]] || [[m:Wikimedia CEE Spring 2026/Structure/Country/Topic|Country/Topic]]
|-
| [[Another Article]] || {{U|Username2}} || Topic3 || Country3 || 2345 || 5309 || [[d:Q789012|Q789012]] ||
|-
|}

== Statistika ==
* '''Kopējais rakstu skaits:''' 523
* '''Dalībnieku skaits:''' 45
* '''Dažādu tēmu skaits:''' 12
* '''Dažādu valstu skaits:''' 25
```

### 2. Participant Report (`participant_report.txt`)

Organized by participant with their contributions:

```wikitext
== Dalībnieku saraksts ==
=== {{U|Username}} ===
Rakstu skaits: 5

* [[Article 1]] - Tēmas: History; Valstis: Latvia; Lasāmais teksts: 1234 rakstzīmes
* [[Article 2]] - Tēmas: Culture; Valstis: Estonia; Lasāmais teksts: 2345 rakstzīmes
```

### 3. Validation Report (`validation_report.txt`)

Data quality and validation information:

```
✅ All data validation checks passed!

WARNINGS:
⚠️  Most common topics: History (45), Culture (32), Politics (28)
⚠️  Most common countries: Latvia (67), Estonia (45), Lithuania (34)
```

### 4. Cache File (`cee_spring_2026_cache.json`)

JSON file containing all collected data for reuse and backup.

## 🛠️ Configuration

Key settings in [`src/config.py`](src/config.py):

```python
# Contest settings
CONTEST_TEMPLATE = "CEE Spring 2026"
CONTEST_YEAR = "2026"

# API settings
MEDIAWIKI_API_URL = "https://lv.wikipedia.org/w/api.php"
API_RATE_LIMIT = 1.0  # requests per second

# Output files
OUTPUT_FILE = f"output/cee_spring_{CONTEST_YEAR}_results.txt"
CACHE_FILE = f"cache/cee_spring_{CONTEST_YEAR}_cache.json"
```

## 📝 Template Format

The tool expects templates in this format on article talk pages:

```wikitext
{{CEE Spring 2026
|dalībnieks = Username
|tēma       = Topic
|tēma2      = Second Topic (optional)
|tēma3      = Third Topic (optional)
|valsts     = Country
|valsts2    = Second Country (optional)
|valsts3    = Third Country (optional)
}}
```

## 🏗️ Architecture

The tool consists of several modular components:

### Core Components

1. **[`src/mediawiki_client.py`](src/mediawiki_client.py)**: MediaWiki API client with rate limiting
2. **[`src/template_parser.py`](src/template_parser.py)**: Template parsing and text analysis
3. **[`src/report_generator.py`](src/report_generator.py)**: Wikitext report generation
4. **[`src/data_validator.py`](src/data_validator.py)**: Data validation and duplicate detection
5. **[`cee_spring_stats.py`](cee_spring_stats.py)**: Main orchestration script

### Data Flow

```
1. Find articles with CEE Spring template (talk pages)
2. Extract template data (participant, topics, countries)
3. Fetch article content and metadata
4. Calculate readable text length
5. Validate and clean data
6. Generate reports in wikitext format
```

## 🧪 Testing

The project includes comprehensive tests:
- API connectivity tests
- Template parsing validation
- Suggested articles integration
- Data validation checks

Run the main test suite:
```bash
python tests/test_tool.py

# Test suggested articles integration
python tests/test_suggested_integration.py
```

## 🔧 Customization

### For Different Contest Years

1. Update [`src/config.py`](src/config.py):
   ```python
   CONTEST_TEMPLATE = "CEE Spring 2027"
   CONTEST_YEAR = "2027"
   ```

2. Update template field mappings if needed:
   ```python
   TEMPLATE_FIELDS = {
       'dalībnieks': 'participant',
       'tēma': 'topic',
       'valsts': 'country',
       # Add new fields as needed
   }
   ```

### For Different Languages

1. Change the MediaWiki API URL:
   ```python
   MEDIAWIKI_API_URL = "https://en.wikipedia.org/w/api.php"
   ```

2. Update talk page prefix in [`src/mediawiki_client.py`](src/mediawiki_client.py):
   ```python
   def _talk_to_article_title(self, talk_title: str) -> Optional[str]:
       if talk_title.startswith('Talk:'):  # English Wikipedia
           return talk_title[5:]
       return None
   ```

### Adding New Metrics

Extend [`src/template_parser.py`](src/template_parser.py) to calculate additional metrics:

```python
def calculate_reference_count(self, wikitext: str) -> int:
    """Count the number of references in the article."""
    ref_pattern = r'<ref[^>]*>.*?</ref>'
    return len(re.findall(ref_pattern, wikitext, re.DOTALL | re.IGNORECASE))
```

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check internet connection
   - Verify the MediaWiki API URL is correct
   - Ensure rate limiting is not too aggressive

2. **Template Not Found**
   - Verify the template name is correct
   - Check if the template exists on the target Wikipedia
   - Ensure articles have the template on talk pages, not main pages

3. **Parsing Errors**
   - Check template format matches expected structure
   - Look for unusual characters or formatting in templates
   - Review validation report for specific issues

4. **Memory Issues with Large Datasets**
   - Process articles in smaller batches
   - Increase system memory
   - Use caching to avoid reprocessing

### Debug Mode

Add debug output by modifying the rate limit in [`src/config.py`](src/config.py):

```python
API_RATE_LIMIT = 0.5  # Slower rate for debugging
```

## 📚 Documentation

See [`docs/USAGE_EXAMPLES.md`](docs/USAGE_EXAMPLES.md) for detailed usage examples and advanced features.

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass: `python tests/test_tool.py`

## 📄 License

This tool is designed for Wikipedia contest analysis and follows Wikipedia's terms of use. Please respect Wikipedia's API terms of service and rate limits.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the validation report for data quality issues
3. Test individual components using [`tests/test_tool.py`](tests/test_tool.py)
4. Check Wikipedia's API documentation for MediaWiki-specific issues

---

**Note**: This tool is designed specifically for the CEE Spring contest on Latvian Wikipedia but can be adapted for other contests and languages with minimal configuration changes.