"""Test script to verify multiple topics parsing functionality."""

from template_parser import TemplateParser


def test_multiple_topics():
    """Test parsing template with multiple topics (tēma, tēma2, tēma3)."""
    print("Testing multiple topics parsing...")

    # Sample template with multiple topics
    sample_template = f"""
{{{{{CONTEST_TEMPLATE}
|dalībnieks = Votre Provocateur
|tēma     = Sievietes
|tēma2    = kultūra
|valsts     = Čuvašija
}}}}
"""

    parser = TemplateParser()
    result = parser.parse_cee_spring_template(sample_template)

    if result:
        print("✅ Multiple topics parsing successful:")
        print(f"  Participant: {result.get('participant')}")
        print(f"  Topics: {result.get('topics')}")
        print(f"  Countries: {result.get('countries')}")

        # Verify we got both topics
        topics = result.get('topics', [])
        if len(topics) == 2 and 'Sievietes' in topics and 'kultūra' in topics:
            print("✅ Both topics correctly parsed!")
            return True
        else:
            print(f"❌ Expected 2 topics ['Sievietes', 'kultūra'], got: {topics}")
            return False
    else:
        print("❌ Template parsing failed")
        return False


def test_three_topics():
    """Test parsing template with three topics."""
    print("\nTesting three topics parsing...")

    # Sample template with three topics
    sample_template = f"""
{{{{{CONTEST_TEMPLATE}
|dalībnieks = TestUser
|tēma     = Vēsture
|tēma2    = Politika
|tēma3    = Kultūra
|valsts   = Latvija
|valsts2  = Igaunija
}}
"""

    parser = TemplateParser()
    result = parser.parse_cee_spring_template(sample_template)

    if result:
        print("✅ Three topics parsing successful:")
        print(f"  Participant: {result.get('participant')}")
        print(f"  Topics: {result.get('topics')}")
        print(f"  Countries: {result.get('countries')}")

        # Verify we got all three topics
        topics = result.get('topics', [])
        expected_topics = ['Vēsture', 'Politika', 'Kultūra']
        if len(topics) == 3 and all(topic in topics for topic in expected_topics):
            print("✅ All three topics correctly parsed!")
            return True
        else:
            print(f"❌ Expected 3 topics {expected_topics}, got: {topics}")
            return False
    else:
        print("❌ Template parsing failed")
        return False


def test_mixed_parameters():
    """Test parsing template with mixed parameter order."""
    print("\nTesting mixed parameter order...")

    # Sample template with mixed order
    sample_template = f"""
{{{{{CONTEST_TEMPLATE}
|valsts2    = Rumānija
|tēma2      = Sabiedrība
|dalībnieks = MixedUser
|valsts     = Ukraina
|tēma       = Vēsture
|valsts3    = Bulgārija
}}
"""

    parser = TemplateParser()
    result = parser.parse_cee_spring_template(sample_template)

    if result:
        print("✅ Mixed parameters parsing successful:")
        print(f"  Participant: {result.get('participant')}")
        print(f"  Topics: {result.get('topics')}")
        print(f"  Countries: {result.get('countries')}")

        # Verify we got the data correctly
        topics = result.get('topics', [])
        countries = result.get('countries', [])

        if ('Vēsture' in topics and 'Sabiedrība' in topics and
            'Ukraina' in countries and 'Rumānija' in countries and 'Bulgārija' in countries):
            print("✅ Mixed parameters correctly parsed!")
            return True
        else:
            print(f"❌ Some parameters not parsed correctly")
            return False
    else:
        print("❌ Template parsing failed")
        return False


def main():
    """Run all multiple topics tests."""
    print("=" * 60)
    print("MULTIPLE TOPICS PARSING - TEST SUITE")
    print("=" * 60)

    tests_passed = 0
    total_tests = 3

    # Test 1: Two topics
    if test_multiple_topics():
        tests_passed += 1

    # Test 2: Three topics
    if test_three_topics():
        tests_passed += 1

    # Test 3: Mixed parameter order
    if test_mixed_parameters():
        tests_passed += 1

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("🎉 All multiple topics tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Multiple topics parsing needs fixes.")
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
