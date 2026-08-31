#!/usr/bin/env python3
"""Validate release 0.19 living marks and podcast corpus registration."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from apply_iteration_19 import EPISODE_COUNT, GENERATED, MARK_COUNT, RELEASE

SUCCESSOR_RELEASE = "0.20-prior-maps-alpha"
SUCCESSOR_GENERATED = "2026-08-25"
CURRENT_RELEASE = "0.21"
CURRENT_GENERATED = "2026-08-31"
HOTFIX_RELEASE = "0.20.2-reader-hotfix"

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "public-data.json"
MANIFEST = ROOT / "docs" / "assets" / "living-marks" / "manifest.json"
LEDGER = ROOT / "docs" / "assets" / "living-marks" / "source-ledger.json"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    if meta.get("release") not in {RELEASE, SUCCESSOR_RELEASE, CURRENT_RELEASE}:
        errors.append(f"meta.release must be {RELEASE}, {SUCCESSOR_RELEASE} or {CURRENT_RELEASE}")
    if meta.get("generated") not in {GENERATED, SUCCESSOR_GENERATED, CURRENT_GENERATED}:
        errors.append(f"meta.generated must be {GENERATED}, {SUCCESSOR_GENERATED} or {CURRENT_GENERATED}")
    if meta.get("living_mark_count") != MARK_COUNT:
        errors.append(f"living_mark_count must be {MARK_COUNT}")
    if meta.get("complexity_podcast_episode_count") != EPISODE_COUNT:
        errors.append(f"complexity_podcast_episode_count must be {EPISODE_COUNT}")
    if meta.get("visual_identity_contract") != "living-marks-v1":
        errors.append("visual identity contract is missing")

    browser = json.loads(read("docs/assets/public-data.json"))
    if browser != data:
        errors.append("browser public-data JSON differs from canonical data")

    sources = {item.get("id") for item in data.get("sources", [])}
    required_sources = {
        "src_sfi_complexity_podcast_archive_2026",
        "src_sfi_complexity_simplecast_2026",
        "src_sfi_complexity_rss_2026",
    }
    missing = required_sources - sources
    if missing:
        errors.append(f"podcast corpus sources missing: {sorted(missing)}")

    nodes = {item.get("id"): item for item in data.get("nodes", []) if item.get("id")}
    podcast = nodes.get("publication_the_complexity_podcast")
    if not podcast or podcast.get("publication_level") != "profile":
        errors.append("developed Complexity Podcast entry is missing")
    profiles = {item.get("node_id") for item in data.get("profiles", [])}
    if "publication_the_complexity_podcast" not in profiles:
        errors.append("Complexity Podcast profile is missing")
    edges = {item.get("id") for item in data.get("edges", [])}
    if "e19_sfi_publishes_complexity_podcast" not in edges:
        errors.append("SFI publication edge is missing")

    corpus = data.get("complexity_podcast_corpus", {})
    if corpus.get("release") != RELEASE or corpus.get("episode_count") != EPISODE_COUNT:
        errors.append("Complexity Podcast corpus register is stale or incomplete")
    if "appearance" not in corpus.get("caution", ""):
        errors.append("podcast corpus caution must distinguish appearance from evidence")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    marks = manifest.get("marks", [])
    if manifest.get("release") != HOTFIX_RELEASE or len(marks) != MARK_COUNT:
        errors.append("living-mark manifest is stale or incomplete")
    if manifest.get("source_media_count") != MARK_COUNT:
        errors.append("living-mark source count is stale")
    ids = [mark.get("id") for mark in marks]
    if len(ids) != len(set(ids)):
        errors.append("living-mark ids are not unique")
    kinds = {mark.get("kind") for mark in marks}
    if kinds != {"image", "video"}:
        errors.append("manifest must contain still and moving marks")
    for mark in marks:
        for key in ("id", "kind", "src", "label", "description", "source_file", "source_sha256"):
            if not mark.get(key):
                errors.append(f"living mark {mark.get('id')!r} lacks {key}")
        asset = ROOT / "docs" / mark.get("src", "")
        if not asset.is_file():
            errors.append(f"living-mark asset missing: {mark.get('src')}")
        elif asset.stat().st_size > 600_000:
            errors.append(f"living-mark asset is too large: {mark.get('src')}")
        if mark.get("kind") == "video":
            poster = ROOT / "docs" / mark.get("poster", "")
            if not poster.is_file():
                errors.append(f"video poster missing: {mark.get('poster')}")
            try:
                probe = json.loads(subprocess.check_output([
                    "ffprobe", "-v", "error", "-show_streams", "-of", "json", str(asset),
                ], text=True))
                streams = probe.get("streams", [])
                video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
                audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
                if len(video_streams) != 1 or video_streams[0].get("codec_name") != "h264":
                    errors.append(f"video mark must contain one H.264 stream: {mark.get('src')}")
                elif video_streams[0].get("width") != 384 or video_streams[0].get("height") != 384:
                    errors.append(f"video mark must be 384 x 384: {mark.get('src')}")
                if audio_streams:
                    errors.append(f"video mark must not contain audio: {mark.get('src')}")
            except (FileNotFoundError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
                errors.append(f"video mark could not be inspected: {mark.get('src')} ({exc})")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    ledger_items = ledger.get("items", [])
    if ledger.get("release") != HOTFIX_RELEASE or ledger.get("source_media_count") != MARK_COUNT:
        errors.append("living-mark source ledger is stale")
    if ledger.get("published_mark_count") != MARK_COUNT or len(ledger_items) != MARK_COUNT:
        errors.append("living-mark source ledger is incomplete")
    if ledger.get("published_existing_count") != 10 or ledger.get("published_new_count") != 74:
        errors.append("living-mark source dispositions do not match the reviewed intake")
    if ledger.get("duplicate_count") != 0 or ledger.get("rejected_count") != 0:
        errors.append("living-mark source ledger contains an unexpected omission")
    ledger_sources = [item.get("source_file") for item in ledger_items]
    if len(ledger_sources) != len(set(ledger_sources)):
        errors.append("living-mark source ledger contains duplicate source files")
    if set(ledger_sources) != {mark.get("source_file") for mark in marks}:
        errors.append("living-mark manifest and source ledger disagree")

    index = read("docs/index.html")
    css = read("docs/assets/iteration-19.css")
    js = read("docs/assets/iteration-19.js")
    for marker in (
        'data-living-mark',
        'assets/iteration-19.css?v=0.20.2-reader-hotfix',
        'assets/iteration-19.js?v=0.20.2-reader-hotfix',
        'The mark is a family, not a badge',
        'class="brand-mark tangle-mark"',
        'data-update-thread-dot',
    ):
        if marker not in index:
            errors.append(f"0.19 interface marker missing: {marker}")
    for marker in ("crypto.getRandomValues", "sessionStorage", "prefers-reduced-motion", "video.muted = true", "video.playsInline = true", "manifest.json"):
        if marker not in js:
            errors.append(f"living-mark behaviour missing: {marker}")
    for marker in ("[data-living-mark]", "prefers-reduced-motion", "object-fit: contain"):
        if marker not in css:
            errors.append(f"living-mark style missing: {marker}")

    for script in ("docs/assets/iteration-19.js",):
        try:
            subprocess.run(["node", "--check", str(ROOT / script)], check=True, capture_output=True, text=True)
        except FileNotFoundError:
            errors.append("node is unavailable for JavaScript syntax checks")
        except subprocess.CalledProcessError as exc:
            errors.append(f"JavaScript does not parse ({script}): {exc.stderr.strip()}")

    required_docs = {
        "documentation/visual-identity.md": ["family, not a badge", "reduced motion", "magic dot"],
        "documentation/corpora/complexity-podcast.md": ["119", "full transcripts", "guest appearance"],
        "documentation/TANGLE_STATE.md": [CURRENT_RELEASE, "source-owner-reviewed"],
        "documentation/NEXT_WORK.md": ["release 0.21 is complete", "No further production change is authorised"],
        "documentation/feedback-ledger.md": ["Release 0.19 — living marks and Complexity Podcast corpus intake"],
        "docs/corpora/complexity-podcast/index.html": ["The Complexity Podcast", "Source roles", "119"],
        "CITATION.cff": [f"version: {meta.get('release')}", f"date-released: {meta.get('generated')}"],
        "README.md": ["Release 0.21", "/corpora/complexity-podcast/"],
        "CHANGELOG.md": [RELEASE],
    }
    for path, markers in required_docs.items():
        text = read(path)
        for marker in markers:
            if marker not in text:
                errors.append(f"required marker missing from {path}: {marker}")

    if errors:
        print("Release 0.19 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validated {RELEASE}: {MARK_COUNT} living marks and {EPISODE_COUNT} podcast feed items registered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
