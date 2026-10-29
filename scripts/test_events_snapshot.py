"""Regression checks for pinned interfaces carrying older collected events."""
from pathlib import Path
import json
import tempfile
import unittest

from events_snapshot import copy_events_interface


class EventsSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='tangle-events-')
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.source, self.target = root / 'source', root / 'target'

    def snapshot(self, root, stamp, marker):
        for folder in ['data', 'feeds', 'assets/data']:
            (root / folder).mkdir(parents=True, exist_ok=True)
        (root / 'data/events.json').write_text(json.dumps({'generatedAt': stamp, 'events': [marker]}), encoding='utf-8')
        (root / 'data/health.json').write_text(marker, encoding='utf-8')
        (root / 'feeds/all.ics').write_text(marker, encoding='utf-8')
        (root / 'index.html').write_text(marker, encoding='utf-8')
        (root / 'assets/data/interface.json').write_text(marker, encoding='utf-8')

    def check_copy(self, source_date, target_date, preserve):
        self.snapshot(self.source, source_date, 'source')
        self.snapshot(self.target, target_date, 'target')
        self.assertEqual(copy_events_interface(self.source, self.target), preserve)
        expected = 'target' if preserve else 'source'
        self.assertEqual(json.loads((self.target / 'data/events.json').read_text(encoding='utf-8'))['events'], [expected])
        self.assertEqual((self.target / 'data/health.json').read_text(encoding='utf-8'), expected)
        self.assertEqual((self.target / 'feeds/all.ics').read_text(encoding='utf-8'), expected)
        self.assertEqual((self.target / 'index.html').read_text(encoding='utf-8'), 'source')
        self.assertEqual((self.target / 'assets/data/interface.json').read_text(encoding='utf-8'), 'source')

    def test_newer_target_keeps_data_and_feeds_but_updates_interface(self):
        self.check_copy('2026-10-17T12:00:00Z', '2026-10-24T12:00:00Z', True)

    def test_newer_source_updates_both_snapshot_directories(self):
        self.check_copy('2026-10-24T12:00:00Z', '2026-10-17T12:00:00Z', False)

    def test_equal_dates_use_source(self):
        self.check_copy('2026-10-24T12:00:00Z', '2026-10-24T12:00:00Z', False)

    def test_dates_are_compared_as_instants(self):
        self.check_copy('2026-10-24T18:00:00Z', '2026-10-24T20:00:00+03:00', False)

    def test_invalid_target_date_allows_source(self):
        self.check_copy('2026-10-24T12:00:00Z', 'invalid', False)

    def test_missing_target_date_allows_source(self):
        self.check_copy('2026-10-24T12:00:00Z', None, False)

    def test_unknown_source_date_does_not_replace_dated_target(self):
        self.check_copy(None, '2026-10-24T12:00:00Z', True)

    def test_missing_target_is_created(self):
        self.snapshot(self.source, '2026-10-24T12:00:00Z', 'source')
        self.assertFalse(copy_events_interface(self.source, self.target))
        self.assertTrue((self.target / 'feeds/all.ics').is_file())


if __name__ == '__main__':
    unittest.main()
