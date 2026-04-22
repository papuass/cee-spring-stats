"""Unit tests for batched page content fetching."""

from unittest.mock import patch, MagicMock
from src.mediawiki_client import MediaWikiClient
from src.suggested_articles import SuggestedArticlesCollector


def _make_page(title, content):
    return {
        'title': title,
        'revisions': [{'slots': {'main': {'content': content}}}]
    }


def _make_missing_page(title):
    return {'title': title, 'missing': True}


def test_get_pages_content_talk_namespace():
    """Talk-page titles are prefixed and results mapped back to original titles."""
    client = MediaWikiClient()

    fake_response = {
        'query': {
            'pages': [
                _make_page('Diskusija:Alpha', 'alpha content'),
                _make_page('Diskusija:Beta', 'beta content'),
            ]
        }
    }

    with patch.object(client, '_make_request', return_value=fake_response) as mock_req:
        result = client.get_pages_content(['Alpha', 'Beta'], namespace=1)

    assert result == {'Alpha': 'alpha content', 'Beta': 'beta content'}
    called_titles = mock_req.call_args[0][0]['titles']
    assert 'Diskusija:Alpha' in called_titles
    assert 'Diskusija:Beta' in called_titles


def test_get_pages_content_missing_page():
    """Missing pages map to None, present pages return content."""
    client = MediaWikiClient()

    fake_response = {
        'query': {
            'pages': [
                _make_page('Present', 'some content'),
                _make_missing_page('Missing'),
            ]
        }
    }

    with patch.object(client, '_make_request', return_value=fake_response):
        result = client.get_pages_content(['Present', 'Missing'], namespace=0)

    assert result['Present'] == 'some content'
    assert result['Missing'] is None


def test_get_pages_content_batches_at_50():
    """Titles are split into batches of 50, one request per batch."""
    client = MediaWikiClient()
    titles = [f'Article{i}' for i in range(110)]

    def fake_request(params):
        batch = params['titles'].split('|')
        return {'query': {'pages': [_make_page(t, f'content-{t}') for t in batch]}}

    with patch.object(client, '_make_request', side_effect=fake_request) as mock_req:
        result = client.get_pages_content(titles, namespace=0)

    assert mock_req.call_count == 3  # ceil(110/50) = 3
    assert len(result) == 110
    assert result['Article0'] == 'content-Article0'
    assert result['Article109'] == 'content-Article109'


def test_get_page_content_delegates_to_batch():
    """Single-title get_page_content still works via the batch method."""
    client = MediaWikiClient()

    fake_response = {
        'query': {
            'pages': [_make_page('MyPage', 'my content')]
        }
    }

    with patch.object(client, '_make_request', return_value=fake_response):
        result = client.get_page_content('MyPage', namespace=0)

    assert result == 'my content'


def test_suggested_articles_batch_fetch():
    """SuggestedArticlesCollector fetches all country pages in one request."""
    collector = SuggestedArticlesCollector()

    fake_response = {
        'query': {
            'pages': [
                _make_page('Wikimedia CEE Spring 2026/Structure/Latvia', '{{#invoke:WikimediaCEETable|table|Q100|Q200}}'),
                _make_page('Wikimedia CEE Spring 2026/Structure/Estonia', '{{#invoke:WikimediaCEETable|table|Q300}}'),
            ]
        }
    }

    with patch.object(collector, '_make_request', return_value=fake_response) as mock_req:
        pages = [
            'Wikimedia CEE Spring 2026/Structure/Latvia',
            'Wikimedia CEE Spring 2026/Structure/Estonia',
        ]
        result = collector.get_pages_content(pages)

    assert mock_req.call_count == 1
    assert 'Wikimedia CEE Spring 2026/Structure/Latvia' in result
    assert 'Q100' in result['Wikimedia CEE Spring 2026/Structure/Latvia']
