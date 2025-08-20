"""Test topic name normalization."""

from src.template_parser import TemplateParser
from src.config import CONTEST_TEMPLATE

def test_topic_normalization():
    """Test topic name normalization."""
    parser = TemplateParser()
    
    # Test cases
    test_cases = [
        ("kultūra", "Kultūra"),
        ("sports", "Sports"),
        ("daba un ģeogrāfija", "Daba un ģeogrāfija"),
        ("POLITIKA", "POLITIKA"),
        ("sievietes", "Sievietes"),
        ("  zinātne  ", "Zinātne"),
        ("", ""),
    ]
    
    print("Testing topic normalization:")
    for original, expected in test_cases:
        result = parser._normalize_topic_name(original)
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{original}' -> '{result}' (expected: '{expected}')")
    
    # Test with full template
    sample_template = f"""
{{{{{CONTEST_TEMPLATE}
|dalībnieks = TestUser
|tēma     = kultūra
|tēma2    = sports
|valsts   = Latvija
}}}}
"""
    
    print("\nTesting full template parsing:")
    result = parser.parse_cee_spring_template(sample_template)
    if result:
        print(f"Topics: {result.get('topics')}")
        # Check if topics are properly capitalized
        topics = result.get('topics', [])
        if topics == ['Kultūra', 'Sports']:
            print("✅ Topic normalization working correctly!")
        else:
            print(f"❌ Expected ['Kultūra', 'Sports'], got {topics}")
    else:
        print("❌ Template parsing failed")

if __name__ == '__main__':
    test_topic_normalization()