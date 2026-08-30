.PHONY: build validate serve clean

build:
	python3 scripts/build_public_data.py
	python3 scripts/apply_release_overrides.py
	python3 scripts/apply_constellation_07.py
	python3 scripts/apply_expansion_08.py
	python3 scripts/apply_iteration_09.py
	python3 scripts/apply_iteration_10.py
	python3 scripts/apply_iteration_11.py
	python3 scripts/apply_iteration_12.py
	python3 scripts/apply_iteration_13.py
	python3 scripts/apply_iteration_14.py
	python3 scripts/apply_iteration_15.py
	python3 scripts/refresh_graph_snapshot.py
	python3 scripts/patch_public_site.py
	python3 scripts/patch_constellation_07.py
	python3 scripts/patch_expansion_08.py
	python3 scripts/patch_iteration_09.py
	python3 scripts/patch_iteration_10.py
	python3 scripts/patch_iteration_11.py
	python3 scripts/patch_iteration_12.py
	python3 scripts/normalise_iteration_11_dot.py
	python3 scripts/patch_iteration_13.py
	python3 scripts/patch_iteration_14.py
	python3 scripts/patch_iteration_15.py
	python3 scripts/prepare_map_hotfix_19.py
	python3 scripts/patch_map_usability_hotfix.py
	python3 scripts/apply_iteration_16.py
	python3 scripts/apply_relational_depth_16.py
	python3 scripts/apply_overnight_review.py
	python3 scripts/apply_adversarial_review.py
	python3 scripts/apply_doncaster_lineage.py
	python3 scripts/refresh_graph_snapshot.py
	python3 scripts/patch_iteration_16.py
	python3 scripts/patch_overnight_experience.py
	python3 scripts/patch_adversarial_experience.py
	python3 scripts/apply_iteration_17.py
	python3 scripts/refresh_graph_snapshot.py
	python3 scripts/patch_iteration_17.py
	python3 scripts/sync_release_docs_17.py
	python3 scripts/apply_iteration_18.py
	python3 scripts/finalise_public_entries_18.py
	python3 scripts/stamp_current_projections_18.py
	python3 scripts/finalise_observation_compat_18.py
	python3 scripts/refresh_graph_snapshot.py
	python3 scripts/patch_iteration_18.py
	python3 scripts/sync_release_docs_18.py
	python3 scripts/finalise_work_spine_18.py
	python3 scripts/patch_validator_compat_18.py
	python3 scripts/build_public_knowledge.py
	python3 scripts/finalise_public_interface_18.py
	python3 scripts/apply_iteration_19.py
	python3 scripts/stamp_current_projections_19.py
	python3 scripts/refresh_relational_document_19.py
	python3 scripts/build_public_knowledge.py
	python3 scripts/refresh_graph_snapshot.py
	python3 scripts/patch_validator_compat_19.py
	python3 scripts/patch_iteration_19.py
	python3 scripts/repair_map_links_19.py
	python3 scripts/apply_castellani_complexity_map.py
	python3 scripts/refresh_graph_snapshot.py
	python3 scripts/build_systemic_evolution_reconciliation.py
	python3 scripts/apply_prior_maps_20.py
	python3 scripts/build_public_knowledge.py
	python3 scripts/refresh_graph_snapshot.py
	python3 scripts/patch_validator_compat_20.py
	python3 scripts/prepare_reader_203_deployment.py

validate:
	python3 scripts/validate_work_spine.py
	python3 scripts/validate_public.py
	python3 scripts/validate_constellation.py
	python3 scripts/validate_expansion_08.py
	python3 scripts/validate_iteration_09.py
	python3 scripts/validate_iteration_10.py
	python3 scripts/validate_iteration_11.py
	python3 scripts/validate_iteration_12.py
	python3 scripts/validate_iteration_13.py
	python3 scripts/finalise_public_interface_18.py
	python3 scripts/validate_iteration_14.py
	python3 scripts/validate_iteration_15.py
	python3 scripts/validate_map_usability_hotfix.py
	python3 scripts/validate_iteration_16.py
	python3 scripts/validate_overnight_experience.py
	python3 scripts/validate_adversarial_review.py
	python3 scripts/validate_doncaster_lineage.py
	python3 scripts/validate_iteration_17.py
	python3 scripts/validate_iteration_18.py
	python3 scripts/patch_iteration_19.py
	python3 scripts/validate_iteration_19.py
	python3 scripts/validate_prior_maps_20.py
	python3 scripts/prepare_reader_203_deployment.py
	./scripts/check_javascript.sh

serve: build
	python3 -m http.server 8000 --directory docs

clean:
	rm -rf validation/*.png validation/*.txt
