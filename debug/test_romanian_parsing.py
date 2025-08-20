#!/usr/bin/env python3
"""
Debug script to test Wikidata ID extraction from Romanian page content.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.suggested_articles import SuggestedArticlesCollector

def test_romanian_parsing():
    """Test parsing of Romanian page content with HTML comments."""
    
    print("=== Testing Romanian format (with HTML comments) ===")
    
    # Sample content from the Romanian page
    romanian_content = """
=== [[File:P art-green.png|30px]] '''Culture''' ===
{{#invoke:WikimediaCEETable|table<!--
RO-->|Q18539344|Q12730061|Q12736402|Q12741766|Q20479854|Q3295106|Q1502282|Q130108154|Q121200137|Q5584324<!--
MD-->|Q12730266|Q28589212|Q128603529|Q110127447}}

=== [[File:P biology-green.png|30px]] '''Nature / Geography''' ===
{{#invoke:WikimediaCEETable|table<!--
RO-->|Q929095|Q3078828|Q3081107|Q12731895<!--
MD-->|Q6271715|Q28861917|Q28721500}}
"""
    
    collector = SuggestedArticlesCollector()
    wikidata_ids = collector.extract_wikidata_ids_from_content(romanian_content)
    
    print(f"Found {len(wikidata_ids)} Wikidata IDs from Romanian format:")
    for qid in sorted(wikidata_ids):
        print(f"  {qid}")
    
    # Expected IDs from the Romanian content
    expected_romanian = {
        'Q18539344', 'Q12730061', 'Q12736402', 'Q12741766', 'Q20479854',
        'Q3295106', 'Q1502282', 'Q130108154', 'Q121200137', 'Q5584324',
        'Q12730266', 'Q28589212', 'Q128603529', 'Q110127447',
        'Q929095', 'Q3078828', 'Q3081107', 'Q12731895',
        'Q6271715', 'Q28861917', 'Q28721500'
    }
    
    if wikidata_ids == expected_romanian:
        print("✅ Romanian format: SUCCESS")
    else:
        print("❌ Romanian format: FAILURE")
        print(f"Expected: {len(expected_romanian)}, Found: {len(wikidata_ids)}")
        missing = expected_romanian - wikidata_ids
        if missing:
            print(f"Missing: {sorted(missing)}")

def test_ukraine_parsing():
    """Test parsing of Ukraine page content without HTML comments."""
    
    print("\n=== Testing Ukraine format (without HTML comments) ===")
    
    # Sample content from Ukraine page
    ukraine_content = """
==== [[File:P art-green.png|30px]] '''Voices of Donetsk Oblast''' ====

{{#invoke:WikimediaCEETable|table|Q237276|Q6351|Q3350307|Q85989211|Q4244705|Q2033316|Q30238440|Q4424614|Q1988030|Q640995}}

{{#invoke:WikimediaCEETable|table|Q12111436|Q4480299|Q4458479|Q426509|Q12111100|Q3888681|Q4059753|Q2025771}}

==== [[File:P art-green.png|30px]] '''Voices of Luhansk Oblast''' ====

{{#invoke:WikimediaCEETable|table|Q640995|Q545793|Q458209|Q4154638|Q28484008|Q14637670|Q7453603|Q51129696}}
"""
    
    collector = SuggestedArticlesCollector()
    wikidata_ids = collector.extract_wikidata_ids_from_content(ukraine_content)
    
    print(f"Found {len(wikidata_ids)} Wikidata IDs from Ukraine format")
    
    # Expected IDs from the Ukraine content
    expected_ukraine = {
        'Q237276', 'Q6351', 'Q3350307', 'Q85989211', 'Q4244705', 'Q2033316',
        'Q30238440', 'Q4424614', 'Q1988030', 'Q640995', 'Q12111436', 'Q4480299',
        'Q4458479', 'Q426509', 'Q12111100', 'Q3888681', 'Q4059753', 'Q2025771',
        'Q545793', 'Q458209', 'Q4154638', 'Q28484008', 'Q14637670', 'Q7453603',
        'Q51129696'
    }
    
    if wikidata_ids == expected_ukraine:
        print("✅ Ukraine format: SUCCESS")
    else:
        print("❌ Ukraine format: FAILURE")
        print(f"Expected: {len(expected_ukraine)}, Found: {len(wikidata_ids)}")
        missing = expected_ukraine - wikidata_ids
        if missing:
            print(f"Missing: {sorted(missing)}")
        extra = wikidata_ids - expected_ukraine
        if extra:
            print(f"Extra: {sorted(extra)}")

def test_lithuanian_parsing():
    """Test parsing of Lithuanian page content."""
    
    print("\n=== Testing Lithuanian format (simple format) ===")
    
    # Sample content from Lithuanian page
    lithuanian_content = """
=== [[File:P biology-green.png|30px]] '''Nature / Geography''' ===
{{#invoke:WikimediaCEETable|table|Q5595|Q1539772|Q648441|Q738428|Q5766077|Q391595|Q4154079|Q5358798|Q1756535|Q1754043|Q1004306|Q847055|Q453700|Q11004650|Q3488554|Q5765225|Q2972120|Q18431394|Q5765594}}

=== [[File:P agriculture-green.png|30px]] '''Economics''' ===
{{#invoke:WikimediaCEETable|table|Q97994672|Q4546952|Q4856416|Q3917352|Q110612892|Q12669432|Q16469123|Q47499312|Q391518|Q16465406|Q796010|Q18745164|Q1341498}}

=== [[File:P transport-green.png|30px]] '''Transport''' ===
{{#invoke:WikimediaCEETable|table|Q581518|Q847711|Q164914|Q429154|Q1740425|Q6707743|Q16458879|Q1567799|Q2935929|Q16443583}}

=== [[File:P transport-green.png|30px]] '''Society''' ===
{{#invoke:WikimediaCEETable|table|Q707346|Q12664573|Q699702|Q1072577|Q6097324|Q12660283|Q932413|Q12652270|Q12676002|Q12657051|Q13030356|Q6756675|Q9369000|Q47329514}}
"""
    
    collector = SuggestedArticlesCollector()
    wikidata_ids = collector.extract_wikidata_ids_from_content(lithuanian_content)
    
    print(f"Found {len(wikidata_ids)} Wikidata IDs from Lithuanian format")
    
    # Expected IDs from the Lithuanian content
    expected_lithuanian = {
        # Nature/Geography
        'Q5595', 'Q1539772', 'Q648441', 'Q738428', 'Q5766077', 'Q391595', 'Q4154079',
        'Q5358798', 'Q1756535', 'Q1754043', 'Q1004306', 'Q847055', 'Q453700',
        'Q11004650', 'Q3488554', 'Q5765225', 'Q2972120', 'Q18431394', 'Q5765594',
        # Economics
        'Q97994672', 'Q4546952', 'Q4856416', 'Q3917352', 'Q110612892', 'Q12669432',
        'Q16469123', 'Q47499312', 'Q391518', 'Q16465406', 'Q796010', 'Q18745164', 'Q1341498',
        # Transport
        'Q581518', 'Q847711', 'Q164914', 'Q429154', 'Q1740425', 'Q6707743',
        'Q16458879', 'Q1567799', 'Q2935929', 'Q16443583',
        # Society
        'Q707346', 'Q12664573', 'Q699702', 'Q1072577', 'Q6097324', 'Q12660283',
        'Q932413', 'Q12652270', 'Q12676002', 'Q12657051', 'Q13030356', 'Q6756675',
        'Q9369000', 'Q47329514'
    }
    
    if wikidata_ids == expected_lithuanian:
        print("✅ Lithuanian format: SUCCESS")
    else:
        print("❌ Lithuanian format: FAILURE")
        print(f"Expected: {len(expected_lithuanian)}, Found: {len(wikidata_ids)}")
        missing = expected_lithuanian - wikidata_ids
        if missing:
            print(f"Missing: {sorted(missing)}")
        extra = wikidata_ids - expected_lithuanian
        if extra:
            print(f"Extra: {sorted(extra)}")

def test_ucdmtable_parsing():
    """Test parsing of UCDMtable format."""
    
    print("\n=== Testing UCDMtable format ===")
    
    # Sample content with UCDMtable format (shortened for testing)
    ucdmtable_content = """
{{#invoke:UCDMtable|table|Q4051116|Q4456215|Q30965709|Q21573827|Q12086505|Q4074981|Q108294310|Q56375918|Q2622781|Q23656293|Q25442872|Q12088959|Q56366780|Q12131555|Q1968021|Q12113171|Q2011217|Q4512017|Q25421031|Q200892}}
"""
    
    collector = SuggestedArticlesCollector()
    wikidata_ids = collector.extract_wikidata_ids_from_content(ucdmtable_content)
    
    print(f"Found {len(wikidata_ids)} Wikidata IDs from UCDMtable format")
    
    # Expected IDs from the sample
    expected_ucdm = {
        'Q4051116', 'Q4456215', 'Q30965709', 'Q21573827', 'Q12086505', 'Q4074981',
        'Q108294310', 'Q56375918', 'Q2622781', 'Q23656293', 'Q25442872', 'Q12088959',
        'Q56366780', 'Q12131555', 'Q1968021', 'Q12113171', 'Q2011217', 'Q4512017',
        'Q25421031', 'Q200892'
    }
    
    if wikidata_ids == expected_ucdm:
        print("✅ UCDMtable format: SUCCESS")
    else:
        print("❌ UCDMtable format: FAILURE")
        print(f"Expected: {len(expected_ucdm)}, Found: {len(wikidata_ids)}")
        missing = expected_ucdm - wikidata_ids
        if missing:
            print(f"Missing: {sorted(missing)}")
        extra = wikidata_ids - expected_ucdm
        if extra:
            print(f"Extra: {sorted(extra)}")

if __name__ == "__main__":
    test_romanian_parsing()
    test_ukraine_parsing()
    test_lithuanian_parsing()
    test_ucdmtable_parsing()