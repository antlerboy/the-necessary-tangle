"""Copy the events interface without replacing a newer collected snapshot."""
from datetime import datetime
from pathlib import Path
import json
import shutil

BUNDLE_DIRECTORIES = {'data', 'feeds'}


def generated_at(root):
    try:
        value = json.loads((root / 'data/events.json').read_text(encoding='utf-8')).get('generatedAt')
        if not isinstance(value, str):
            return None
        stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return stamp if stamp.tzinfo is not None else None
    except (OSError, UnicodeError, ValueError, AttributeError):
        return None


def copy_events_interface(source, target):
    """Keep the newer target's data and feeds together; always update the UI.

    A valid target timestamp is retained when the source date is unavailable.
    A missing or invalid target date allows the source snapshot to be copied.
    """
    source, target = Path(source), Path(target)
    source_date, target_date = generated_at(source), generated_at(target)
    preserve = (
        target_date is not None
        and all((target / name).is_dir() for name in BUNDLE_DIRECTORIES)
        and (source_date is None or target_date > source_date)
    )
    source_root = source.resolve()

    def ignore(directory, names):
        if preserve and Path(directory).resolve() == source_root:
            return BUNDLE_DIRECTORIES.intersection(names)
        return set()

    shutil.copytree(source, target, dirs_exist_ok=True, ignore=ignore)
    return preserve
