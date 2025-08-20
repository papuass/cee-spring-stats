# CEE Spring Statistics Tool

A Python tool for collecting and analyzing statistics from Wikipedia articles participating in the CEE Spring contest. This tool automatically gathers data from articles tagged with the `{{CEE Spring 2025}}` template and generates comprehensive reports in wikitext format.

## Features

- **Automatic Article Discovery**: Finds all articles with the CEE Spring template on their talk pages
- **Template Data Extraction**: Extracts participant names, topics, and countries from contest templates
- **Article Metrics**: Collects article size in bytes and calculates readable text length
- **Data Validation**: Includes duplicate detection and data quality checks
- **Multiple Report Formats**: Generates sortable wikitext tables and participant summaries
- **Caching System**: Saves collected data to avoid re-processing
- **Rate Limiting**: Respects Wikipedia's API guidelines

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

Run the tool to collect all CEE Spring 2025 statistics:

```bash
python cee_spring_stats.py
```

This will:
1. Search for all articles with the `{{CEE Spring 2025}}` template
2. Extract participant and topic data from talk pages
3. Calculate article metrics (size, readable text length)
4. Generate wikitext reports
5. Save results to files

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
python test_tool.py
```

This will verify:
- API connection to Latvian Wikipedia
- Template search functionality
- Data parsing capabilities
- Single article processing

## Configuration

Edit [`config.py`](config.py) to customize the tool:

```python
# Contest settings
CONTEST_TEMPLATE = "CEE Spring 2025"
CONTEST_YEAR = "2025"

# API settings
MEDIAWIKI_API_URL = "https://lv.wikipedia.org/w/api.php"
API_RATE_LIMIT = 1.0  # requests per second

# Output files
OUTPUT_FILE = f"cee_spring_{CONTEST_YEAR}_results.txt"
CACHE_FILE = f"cee_spring_{CONTEST_YEAR}_cache.json"
```

## Output Files

The tool generates several output files:

### 1. Main Results (`cee_spring_2025_results.txt`)

A wikitext table ready for publishing on Wikipedia:

```wikitext
== Konkursā iesniegtie raksti ==
{| class="sortable wikitable"
|-
! Raksts !! Dalībnieks !! 1. tēma !! 2. tēma !! 3. tēma !! 1. valsts !! 2. valsts !! 3. valsts !! Lasāmā teksta garums !! Raksta garums baitos
|-
| [[Article Title]] || {{U|Username}} || Topic1 || Topic2 || Topic3 || Country1 || Country2 || Country3 || 1234 || {{PAGESIZE:Article Title}}
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

### 4. Cache File (`cee_spring_2025_cache.json`)

JSON file containing all collected data for reuse and backup.

## Template Format

The tool expects templates in this format on article talk pages:

```wikitext
{{CEE Spring 2025
|dalībnieks = Username
|tēma       = Topic
|tēma2      = Second Topic (optional)
|tēma3      = Third Topic (optional)
|valsts     = Country
|valsts2    = Second Country (optional)
|valsts3    = Third Country (optional)
}}
```

## Architecture

The tool consists of several modular components:

### Core Components

1. **[`mediawiki_client.py`](mediawiki_client.py)**: MediaWiki API client with rate limiting
2. **[`template_parser.py`](template_parser.py)**: Template parsing and text analysis
3. **[`report_generator.py`](report_generator.py)**: Wikitext report generation
4. **[`data_validator.py`](data_validator.py)**: Data validation and duplicate detection
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

## Customization

### For Different Contest Years

1. Update [`config.py`](config.py):
   ```python
   CONTEST_TEMPLATE = "CEE Spring 2026"
   CONTEST_YEAR = "2026"
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

2. Update talk page prefix in [`mediawiki_client.py`](mediawiki_client.py):
   ```python
   def _talk_to_article_title(self, talk_title: str) -> Optional[str]:
       if talk_title.startswith('Talk:'):  # English Wikipedia
           return talk_title[5:]
       return None
   ```

### Adding New Metrics

Extend [`template_parser.py`](template_parser.py) to calculate additional metrics:

```python
def calculate_reference_count(self, wikitext: str) -> int:
    """Count the number of references in the article."""
    ref_pattern = r'<ref[^>]*>.*?</ref>'
    return len(re.findall(ref_pattern, wikitext, re.DOTALL | re.IGNORECASE))
```

## Troubleshooting

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

Add debug output by modifying the rate limit in [`config.py`](config.py):

```python
API_RATE_LIMIT = 0.5  # Slower rate for debugging
```

## Contributing

To contribute to this tool:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `python test_tool.py`
5. Submit a pull request

## License

This tool is provided as-is for Wikipedia contest administration. Please respect Wikipedia's API terms of service and rate limits.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the validation report for data quality issues
3. Test individual components using [`test_tool.py`](test_tool.py)
4. Check Wikipedia's API documentation for MediaWiki-specific issues

---

**Note**: This tool is designed specifically for the CEE Spring contest on Latvian Wikipedia but can be adapted for other contests and languages with minimal configuration changes.