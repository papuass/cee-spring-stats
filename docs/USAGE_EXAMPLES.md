# Usage Examples

This document provides practical examples of how to use the CEE Spring Statistics Tool.

## Example 1: Basic Collection

Collect all CEE Spring 2025 statistics:

```bash
python cee_spring_stats.py
```

**Expected Output:**
```
Starting CEE Spring CEE Spring 2025 statistics collection...
Timestamp: 2025-08-18T13:43:05.062000
Collecting suggested articles from Meta-Wiki...
Found 5077 suggested Wikidata IDs from Meta-Wiki
Collecting data from Wikipedia...
Searching for articles with template: CEE Spring 2025
Found 523 articles with the template.
Fetching page information...
Processing article 1/523: Džagatajs
  ✓ Processed: Treisijs - 1 topics
Processing article 2/523: Anatolijs Šundels
  ✓ Processed: Votre Provocateur - 1 topics
...
Successfully processed 523 articles.
Saved 523 articles to cache.
Validating data...
Validation warnings:
  ⚠️  Most common topics: Vēsture (89), Politika (67), Sabiedrība (45)
  ⚠️  Most common countries: Krievija (123), Ukraina (89), Polija (67)
Generating reports...
Reports generated successfully!
Main report saved to: cee_spring_2025_results.txt
Participant report saved to: participant_report.txt

==================================================
COLLECTION SUMMARY
==================================================
Total articles: 523
Unique participants: 45
Unique topics: 15
Unique countries: 28
Total readable text: 1,234,567 characters
Total article size: 2,345,678 bytes

Top 5 participants:
  1. Votre Provocateur: 89 articles
  2. Egilus: 67 articles
  3. ZANDMANIS: 45 articles
  4. Treisijs: 34 articles
  5. Feens: 23 articles
```

## Example 2: Using Cache

After the initial collection, you can work with cached data:

```bash
# View summary without re-collecting
python cee_spring_stats.py --summary-only
```

```bash
# Force fresh collection (ignore cache)
python cee_spring_stats.py --no-cache
```

```bash
# Collect fresh data but don't update cache
python cee_spring_stats.py --no-cache --no-save-cache
```

## Example 3: Generated Wikitext Output

The main output file (`cee_spring_2025_results.txt`) contains:

```wikitext
== Konkursā iesniegtie raksti ==
{| class="sortable wikitable"
|-
! Raksts !! Dalībnieks !! Tēma !! Valsts !! Lasāmā teksta garums !! Raksta garums baitos !! Wikidata ID !! No ieteikumu saraksta
|-
| [[1978. gada demonstrācijas Gruzijā]] || {{U|Votre Provocateur}} || Vēsture || Gruzija || 820 || 2172 || [[d:Q51846024|Q51846024]] ||
|-
| [[Ahmats Kadirovs]] || {{U|Votre Provocateur}} || Politika || Krievija || 1462 || 3245 || [[d:Q133458940|Q133458940]] || [[m:Wikimedia CEE Spring 2025/Structure/Russia/Politics|Russia/Politics]]
|-
| [[Akmens tilts (Tartu)]] || {{U|Egilus}} || Vēsture || Igaunija || 7312 || 12456 || [[d:Q36831|Q36831]] ||
|-
|}

== Statistika ==
* '''Kopējais rakstu skaits:''' 523
* '''Dalībnieku skaits:''' 45
* '''Dažādu tēmu skaits:''' 15
* '''Dažādu valstu skaits:''' 28
* '''Kopējais lasāmā teksta garums:''' 1,234,567 rakstzīmes
* '''Raksti no ieteikumu saraksta:''' 156 no 523 (29.8%)

=== Aktīvākie dalībnieki ===
1. {{U|Votre Provocateur}} - 89 raksti, 123,456 rakstzīmes
2. {{U|Egilus}} - 67 raksti, 234,567 rakstzīmes
3. {{U|ZANDMANIS}} - 45 raksti, 156,789 rakstzīmes
4. {{U|Treisijs}} - 34 raksti, 98,765 rakstzīmes
5. {{U|Feens}} - 23 raksti, 87,654 rakstzīmes
```

## Example 4: Participant Report

The participant report (`participant_report.txt`) shows:

```wikitext
== Dalībnieku saraksts ==
=== {{U|Egilus}} ===
Rakstu skaits: 67

* [[Akmens tilts (Tartu)]] - Tēmas: Vēsture, Arhitektūra; Valstis: Igaunija; Lasāmais teksts: 7312 rakstzīmes
* [[Cilvēktiesības Slovākijā]] - Tēmas: Cilvēktiesības; Valstis: Slovākija; Lasāmais teksts: 2145 rakstzīmes
* [[Prāgas pavasaris]] - Tēmas: Vēsture, Politika; Valstis: Čehija; Lasāmais teksts: 4567 rakstzīmes

=== {{U|Votre Provocateur}} ===
Rakstu skaits: 89

* [[1978. gada demonstrācijas Gruzijā]] - Tēmas: Vēsture; Valstis: Gruzija; Lasāmais teksts: 820 rakstzīmes
* [[Ahmats Kadirovs]] - Tēmas: Politika; Valstis: Krievija; Lasāmais teksts: 1462 rakstzīmes
* [[Aguli]] - Tēmas: Sabiedrība; Valstis: Krievija; Lasāmais teksts: 338 rakstzīmes
```

## Example 5: Validation Report

The validation report (`validation_report.txt`) might show:

```
WARNINGS:
⚠️  Removed 3 duplicate articles: Duplicate Article 1, Duplicate Article 2, Duplicate Article 3
⚠️  Article 'Some Article' has no topics specified
⚠️  Article 'Another Article' has no countries specified
⚠️  Potential participant name variations: User1, user1
⚠️  Unusually long article: 'Very Long Article' (25000 chars)
⚠️  Most common topics: Vēsture (89), Politika (67), Sabiedrība (45), Kultūra (34), Sports (23)
⚠️  Most common countries: Krievija (123), Ukraina (89), Polija (67), Igaunija (45), Lietuva (34)
```

## Example 6: Testing Before Full Run

Always test the tool first:

```bash
python test_tool.py
```

**Expected Output:**
```
============================================================
CEE SPRING STATISTICS TOOL - TEST SUITE
============================================================
Testing API connection to Latvian Wikipedia...
✅ Successfully connected to: Vikipēdija

Testing template search for: CEE Spring 2025
Found 523 articles with the template
Sample articles found:
  1. Džagatajs
  2. Anatolijs Šundels
  3. Armēnijas revolūcija (2018)
  4. Piramīdu shēmas Albānijā
  5. Irina Fariona
  ... and 518 more articles

Testing template parsing...
✅ Template parsing successful:
  Participant: Votre Provocateur
  Topics: ['Sabiedrība']
  Countries: ['Ukraina', 'Rumānija un Moldova', 'Bulgārija']

Testing single article processing: Džagatajs
✅ Article processing successful:
  Title: Džagatajs
  Participant: Treisijs
  Topics: ['valodniecība']
  Countries: ['starptautiski', 'Uzbekistāna']
  Size (bytes): 2847
  Readable length: 1234

============================================================
TEST SUMMARY
============================================================
Tests passed: 4/4
🎉 All tests passed! The tool is ready to use.

## Example 7: Suggested Articles Integration

The tool automatically collects suggested article lists from Meta-Wiki and identifies which contest articles were created from these suggestions.

### Testing Suggested Articles Integration

```bash
python test_suggested_integration.py
```

**Expected Output:**
```
============================================================
TESTING SUGGESTED ARTICLES INTEGRATION
============================================================
1. Testing suggested articles collection...
Collecting suggested article Wikidata IDs from Meta-Wiki...
Processing 1/29: Albania
  Found 118 suggested articles for Albania
Processing 2/29: Armenia
  Found 149 suggested articles for Armenia
...
Total suggested articles collected: 5077
Countries with suggested articles: 25
✅ Found 5077 suggested Wikidata IDs

2. Testing article processing with suggested check...
   Processing 3 test articles...
   ✓ Džagatajs: Suggested=False, Wikidata=Q36831
   ✓ Anatolijs Šundels: Suggested=False, Wikidata=Q133458940
   ✓ Armēnijas revolūcija (2018): Suggested=False, Wikidata=Q51846024
✅ Processed 3 articles, 0 from suggested lists

3. Testing report generation with suggested column...
✅ Report generation with suggested column works correctly
```

### How Suggested Articles Detection Works

1. **Collection Phase**: The tool fetches all structure pages from Meta-Wiki (e.g., `Wikimedia CEE Spring 2025/Structure/Armenia`)
2. **Extraction**: It extracts Wikidata IDs from `{{#invoke:WikimediaCEETable|table|Q123|Q456|...}}` templates
3. **Matching**: During article processing, it checks if each article's Wikidata ID matches any suggested ID
4. **Reporting**: The results include a "No ieteikumu saraksta" (From Suggested List) column showing a link to the specific suggested topics page when the article is from a suggested list, or empty when it's not

### Suggested Articles Statistics

The reports now include statistics about suggested articles usage:

```wikitext
* '''Raksti no ieteikumu saraksta:''' 156 no 523 (29.8%)
```

This shows how many contest articles were created from the official suggested lists, helping organizers understand the impact of their suggestions.

## Example 8: Multiple Topics Support

The tool now supports multiple topics per article using `tēma`, `tēma2`, and `tēma3` parameters:

### Template with Multiple Topics
```wikitext
{{CEE Spring 2025 
|dalībnieks = Votre Provocateur 
|tēma     = Sievietes 
|tēma2    = kultūra
|valsts     = Čuvašija
}}
```

### Testing Multiple Topics
```bash
python test_multiple_topics.py
```

**Expected Output:**
```
============================================================
MULTIPLE TOPICS PARSING - TEST SUITE
============================================================
Testing multiple topics parsing...
✅ Multiple topics parsing successful:
  Participant: Votre Provocateur
  Topics: ['Sievietes', 'kultūra']
  Countries: ['Čuvašija']
✅ Both topics correctly parsed!

Testing three topics parsing...
✅ Three topics parsing successful:
  Participant: TestUser
  Topics: ['Vēsture', 'Politika', 'Kultūra']
  Countries: ['Latvija', 'Igaunija']
✅ All three topics correctly parsed!

Testing mixed parameter order...
✅ Mixed parameters parsing successful:
  Participant: MixedUser
  Topics: ['Sabiedrība', 'Vēsture']
  Countries: ['Rumānija', 'Ukraina', 'Bulgārija']
✅ Mixed parameters correctly parsed!

============================================================
TEST SUMMARY
============================================================
Tests passed: 3/3
🎉 All multiple topics tests passed!
```

### Generated Output with Multiple Topics
The wikitext table will show all topics in separate columns:

```wikitext
| [[Article Title]] || {{U|Votre Provocateur}} || Sievietes, kultūra || Čuvašija || 1234 || 3710 || [[d:Q123456|Q123456]] || [[m:Wikimedia CEE Spring 2025/Structure/Chuvashia/Culture|Chuvashia/Culture]]
```

**Note**: The tool supports up to 3 topics and 3 countries per article, matching the table format requirements.
```

## Example 7: Customizing for Different Contest

To adapt for CEE Spring 2026:

1. Edit `config.py`:
```python
CONTEST_TEMPLATE = "CEE Spring 2026"
CONTEST_YEAR = "2026"
```

2. Run the tool:
```bash
python cee_spring_stats.py
```

The tool will automatically:
- Search for `{{CEE Spring 2026}}` templates
- Generate `cee_spring_2026_results.txt`
- Create `cee_spring_2026_cache.json`

## Example 8: Working with Large Datasets

For contests with many articles (500+), the tool automatically:

1. **Processes in batches**: API calls are batched for efficiency
2. **Uses caching**: Saves progress to avoid restarting from scratch
3. **Rate limits**: Respects Wikipedia's API guidelines (1 request/second)
4. **Shows progress**: Displays current article being processed

**Estimated Processing Time:**
- 100 articles: ~5 minutes
- 500 articles: ~20 minutes  
- 1000 articles: ~40 minutes

## Example 9: Troubleshooting Common Issues

### Issue: No articles found
```bash
python cee_spring_stats.py
```
```
Starting CEE Spring CEE Spring 2025 statistics collection...
Searching for articles with template: CEE Spring 2025
No articles found with the specified template.
```

**Solution**: Check if the template name is correct in `config.py`

### Issue: API connection failed
```
❌ Failed to connect to API
```

**Solution**: Check internet connection and API URL in `config.py`

### Issue: Template parsing errors
```
⚠️  Article 'Some Article' has invalid topics format
```

**Solution**: Check template format on the article's talk page

## Example 10: Publishing Results

Copy the generated wikitext to Wikipedia:

1. Open the main results file: `cee_spring_2025_results.txt`
2. Copy the entire content
3. Paste into a Wikipedia page (e.g., "Wikipedia:CEE Spring 2025/Results")
4. The sortable table will work automatically with Wikipedia's table sorting
