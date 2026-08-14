#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/public-data.json').read_text(encoding='utf-8'))
meta=D['meta']; assert meta['release']=='0.15-ing-reading-practice-alpha'; assert meta['generated']=='2026-08-14'
node_ids={n['id'] for n in D['nodes']}; profile_ids={p.get('node_id') for p in D['profiles']}; journey_ids={j['id'] for j in D['journeys']}
required_nodes={'person_david_ing','corpus_coevolving_innovations','corpus_systems_changes','approach_family_service_systems_thinking','approach_family_systems_changes_learning','practice_systems_lineage_documentation','publication_pattern_manual_service_systems_thinking','publication_systems_thinkers_ramage_shipp','publication_steps_to_ecology_of_mind','publication_understanding_understanding','publication_flawless_consulting','practice_core_systems_practice_spine'}
assert required_nodes <= node_ids; assert required_nodes <= profile_ids
assert {'journey_david_ing_systems_in_plural','journey_core_systems_practice_reading'} <= journey_ids
inv=D['reading_list_inventory']; assert inv['release']==meta['release']; assert inv['item_count']>=100; assert sum(inv['counts'].values())==inv['item_count']; assert inv['counts']['developed_profile']>=25
core=D['core_systems_practice']; assert len(core['major_approaches'])==4; assert set(core['major_approaches']) <= node_ids
obs=D['ai_observations']; assert obs['release']==meta['release']; ids={o['id'] for o in obs['observations']}; assert {'reading_list_depth','ing_lineage_infrastructure','core_practice_not_four_tools','attention_is_not_importance'} <= ids
index=(ROOT/'docs/index.html').read_text(encoding='utf-8'); assert 'journey_david_ing_systems_in_plural' in index; assert 'journey_core_systems_practice_reading' in index; assert 'reading-list.html' in index; assert 'themeToggle' in index
reading=(ROOT/'docs/reading-list.html').read_text(encoding='utf-8'); assert 'Reading-list depth' in reading; assert 'Inventory-only' in reading; assert str(inv['item_count']) in reading
assert (ROOT/'documentation/core-systems-practice.md').is_file(); assert (ROOT/'documentation/reading-list-coverage.md').is_file()
# One discreet route, inherited from validated 0.14 patching.
update='https://github.com/antlerboy/the-necessary-tangle/issues/2'; assert index.count(update)==1
# Public release must not narrate private production history.
public_paths=[ROOT/'docs/index.html',ROOT/'docs/reading-list.html',ROOT/'documentation/reading-list-coverage.md',ROOT/'documentation/core-systems-practice.md',ROOT/'documentation/ai-observations.md']
for path in public_paths:
    text=path.read_text(encoding='utf-8').casefold()
    for banned in ['chatgpt','openai','this conversation','our conversation','previously omitted','we forgot','i forgot','assistant said']:
        assert banned not in text, (path,banned)
print(json.dumps({'release':meta['release'],'entries':meta['public_entry_count'],'profiles':meta['profile_count'],'sources':meta['source_count'],'journeys':meta['journey_count'],'reading_items':inv['item_count'],'reading_developed':inv['counts']['developed_profile'],'observations':len(obs['observations'])},indent=2))
