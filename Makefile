.PHONY: build validate serve clean

build:
	python3 scripts/build_public_data.py
	python3 scripts/build_public_knowledge.py

validate: build
	python3 scripts/validate_public.py
	./scripts/check_javascript.sh

serve: build
	python3 -m http.server 8000 --directory docs

clean:
	rm -rf validation/*.png validation/*.txt
