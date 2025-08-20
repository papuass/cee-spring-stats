# CEE Spring Statistics Tool

A comprehensive tool for collecting and analyzing statistics from Wikipedia articles submitted to the CEE Spring contest.

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
├── 📁 output/                  # Generated reports and results
│   ├── cee_spring_2025_results.txt   # Main wikitext report
│   ├── participant_report.txt        # Participant breakdown
│   ├── contest_categories.txt        # Contest categories
│   └── validation_report.txt         # Data validation report
├── 📁 cache/                   # Cached data files
│   └── cee_spring_2025_cache.json    # Article data cache
├── 📁 debug/                   # Debug and analysis scripts
│   ├── debug_armenia_duplicates.py   # Armenia duplicates analysis
│   └── debug_page_size.py           # Page size debugging
├── 📁 docs/                    # Documentation
│   ├── README.md              # This file
│   └── USAGE_EXAMPLES.md      # Usage examples and guides
├── cee_spring_stats.py        # Main entry point script
├── requirements.txt           # Python dependencies
└── .env.example              # Environment variables template
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the tool:**
   ```bash
   python cee_spring_stats.py
   ```

3. **View results:**
   - Main report: `output/cee_spring_2025_results.txt`
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

### Using Cache
```bash
# View summary from cache
python cee_spring_stats.py --summary-only

# Force fresh collection
python cee_spring_stats.py --no-cache
```

### Testing
```bash
# Run main test suite
python tests/test_tool.py

# Test suggested articles integration
python tests/test_suggested_integration.py
```

## 📊 Sample Output

The tool generates comprehensive reports including:

- **523 articles** from **24 participants**
- **31 unique topics** across **50 countries**
- **782,628 characters** of readable text
- **29.8%** of articles from suggested lists

## 🛠️ Configuration

Key settings in `src/config.py`:
- Contest template name
- Output file paths
- API rate limiting
- Field mappings

## 🧪 Testing

The project includes comprehensive tests:
- API connectivity tests
- Template parsing validation
- Suggested articles integration
- Data validation checks

## 📚 Documentation

See `docs/USAGE_EXAMPLES.md` for detailed usage examples and advanced features.

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass

## 📄 License

This tool is designed for Wikipedia contest analysis and follows Wikipedia's terms of use.