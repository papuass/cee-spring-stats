#!/usr/bin/env python3
"""
Debug script to test regex pattern matching.
"""

import re

def test_regex_patterns():
    """Test different regex patterns on the Romanian content."""
    
    # Sample content from the Romanian page
    sample_content = """{{#invoke:WikimediaCEETable|table<!--
RO-->|Q18539344|Q12730061|Q12736402|Q12741766|Q20479854|Q3295106|Q1502282|Q130108154|Q121200137|Q5584324<!--
MD-->|Q12730266|Q28589212|Q128603529|Q110127447}}"""
    
    print("Testing content:")
    print(repr(sample_content))
    print()
    
    # Current pattern
    pattern1 = r'\{\{#invoke:WikimediaCEETable\|table[^}]*?\}\}'
    matches1 = re.findall(pattern1, sample_content, re.IGNORECASE | re.DOTALL)
    
    print("Pattern 1 (current):", pattern1)
    print(f"Matches: {len(matches1)}")
    for i, match in enumerate(matches1):
        print(f"  Match {i+1}: {repr(match)}")
    print()
    
    # Alternative pattern - more greedy
    pattern2 = r'\{\{#invoke:WikimediaCEETable\|table.*?\}\}'
    matches2 = re.findall(pattern2, sample_content, re.IGNORECASE | re.DOTALL)
    
    print("Pattern 2 (alternative):", pattern2)
    print(f"Matches: {len(matches2)}")
    for i, match in enumerate(matches2):
        print(f"  Match {i+1}: {repr(match)}")
    print()
    
    # Test Q-ID extraction from the match
    if matches2:
        match = matches2[0]
        print("Testing Q-ID extraction from first match:")
        
        # Remove HTML comments
        clean_match = re.sub(r'<!--[^>]*?-->', '', match)
        print(f"After removing comments: {repr(clean_match)}")
        
        # Split by | and extract Q-IDs
        parts = clean_match.split('|')
        qids = []
        for part in parts:
            part = part.strip()
            if part.startswith('Q') and part[1:].isdigit():
                qids.append(part)
        
        print(f"Found Q-IDs: {qids}")
        print(f"Expected Q110127447: {'Q110127447' in qids}")

if __name__ == "__main__":
    test_regex_patterns()