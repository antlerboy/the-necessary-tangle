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
	python3 scripts/patch_map_usability_hotfix.py
	python3 scripts/apply_iteration_16.py
	python3 scripts/apply_relational_depth_16.py
	python3 scripts/refresh_graph_snapshot.py
	python3 scripts/patch_iteration_16.py
	python3 scripts/build_public_knowledge.py

validate: build
	python3 scripts/validate_public.py
	python3 scripts/validate_constellation.py
	python3 scripts/validate_expansion_08.py
	python3 scripts/validate_iteration_09.py
	python3 scripts/validate_iteration_10.py
	python3 scripts/validate_iteration_11.py
	python3 scripts/validate_iteration_12.py
	python3 scripts/validate_iteration_13.py
	python3 scripts/validate_iteration_14.py
	python3 scripts/validate_iteration_15.py
	python3 scripts/validate_map_usability_hotfix.py
	python3 scripts/validate_iteration_16.py
	./scripts/check_javascript.sh

serve: build
	python3 -m http.server 8000 --directory docs

clean:
	rm -rf validation/*.png validation/*.txt
