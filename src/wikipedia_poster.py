"""Wikipedia page editor for posting CEE Spring stats between marker comments."""

import requests
from typing import Optional
from .config import MEDIAWIKI_API_URL, USER_AGENT


class WikipediaPoster:
    """Handles authentication and section editing of Wikipedia pages."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self.logged_in = False

    def login(self, username: str, password: str) -> bool:
        """
        Log in to Wikipedia using a bot password.

        Args:
            username: Bot username (format: Username@BotName for BotPasswords)
            password: Bot password

        Returns:
            True if login succeeded, False otherwise
        """
        # Step 1: get login token
        params = {
            'action': 'query',
            'meta': 'tokens',
            'type': 'login',
            'format': 'json',
        }
        try:
            resp = self.session.get(MEDIAWIKI_API_URL, params=params, timeout=30)
            resp.raise_for_status()
            login_token = resp.json()['query']['tokens']['logintoken']
        except (requests.RequestException, KeyError) as exc:
            print(f"Failed to get login token: {exc}")
            return False

        # Step 2: log in
        login_data = {
            'action': 'login',
            'lgname': username,
            'lgpassword': password,
            'lgtoken': login_token,
            'format': 'json',
        }
        try:
            resp = self.session.post(MEDIAWIKI_API_URL, data=login_data, timeout=30)
            resp.raise_for_status()
            result = resp.json()
        except (requests.RequestException, KeyError) as exc:
            print(f"Login request failed: {exc}")
            return False

        if result.get('login', {}).get('result') == 'Success':
            self.logged_in = True
            print(f"Logged in as {result['login'].get('lgusername', username)}")
            return True

        reason = result.get('login', {}).get('reason', 'unknown error')
        print(f"Login failed: {reason}")
        return False

    def _get_csrf_token(self) -> Optional[str]:
        """Get a CSRF (edit) token from the current session."""
        params = {
            'action': 'query',
            'meta': 'tokens',
            'format': 'json',
        }
        try:
            resp = self.session.get(MEDIAWIKI_API_URL, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()['query']['tokens']['csrftoken']
        except (requests.RequestException, KeyError) as exc:
            print(f"Failed to get CSRF token: {exc}")
            return None

    def get_page_content(self, title: str) -> Optional[str]:
        """Fetch the raw wikitext of a page."""
        params = {
            'action': 'query',
            'prop': 'revisions',
            'rvprop': 'content',
            'rvslots': 'main',
            'titles': title,
            'format': 'json',
            'formatversion': '2',
        }
        try:
            resp = self.session.get(MEDIAWIKI_API_URL, params=params, timeout=30)
            resp.raise_for_status()
            pages = resp.json()['query']['pages']
        except (requests.RequestException, KeyError) as exc:
            print(f"Failed to fetch page '{title}': {exc}")
            return None

        if not pages:
            return None

        page = pages[0]
        if 'missing' in page:
            print(f"Page not found: {title}")
            return None

        try:
            return page['revisions'][0]['slots']['main']['content']
        except (KeyError, IndexError) as exc:
            print(f"Unexpected page structure: {exc}")
            return None

    def update_between_markers(
        self,
        title: str,
        new_content: str,
        begin_marker: str,
        end_marker: str,
        summary: str = "Automātisks CEE Spring statistikas atjauninājums",
    ) -> bool:
        """
        Replace the text between begin_marker and end_marker on a Wikipedia page.

        Args:
            title: Full page title (e.g. "Vikipēdija:CEE_Spring_2026/Statistika")
            new_content: New wikitext to place between the markers
            begin_marker: Opening HTML comment marker
            end_marker: Closing HTML comment marker
            summary: Edit summary shown in page history

        Returns:
            True if the edit was saved successfully, False otherwise
        """
        if not self.logged_in:
            print("Not logged in — call login() first")
            return False

        current = self.get_page_content(title)
        if current is None:
            return False

        begin_pos = current.find(begin_marker)
        end_pos = current.find(end_marker)

        if begin_pos == -1:
            print(f"Begin marker not found: {begin_marker!r}")
            return False
        if end_pos == -1:
            print(f"End marker not found: {end_marker!r}")
            return False
        if end_pos <= begin_pos:
            print("End marker appears before begin marker")
            return False

        after_begin = begin_pos + len(begin_marker)
        updated = (
            current[:after_begin]
            + "\n"
            + new_content.strip()
            + "\n"
            + current[end_pos:]
        )

        csrf_token = self._get_csrf_token()
        if not csrf_token:
            return False

        edit_data = {
            'action': 'edit',
            'title': title,
            'text': updated,
            'summary': summary,
            'token': csrf_token,
            'format': 'json',
        }
        try:
            resp = self.session.post(MEDIAWIKI_API_URL, data=edit_data, timeout=60)
            resp.raise_for_status()
            result = resp.json()
        except (requests.RequestException, KeyError) as exc:
            print(f"Edit request failed: {exc}")
            return False

        if result.get('edit', {}).get('result') == 'Success':
            nochange = result['edit'].get('nochange') is not None
            if nochange:
                print("No change — page content was already up to date")
            else:
                rev_id = result['edit'].get('newrevid', '?')
                print(f"Page updated successfully (revision {rev_id})")
            return True

        print(f"Edit failed: {result}")
        return False
