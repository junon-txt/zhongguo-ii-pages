.PHONY: build serve deploy

PAGES_BUILD_DIR=pages_build
BUILD_TIMESTAMP=.build-timestamp

check_changes:
	@if [ ! -f $(BUILD_TIMESTAMP) ] || find pages/ -newer $(BUILD_TIMESTAMP) | grep -q .; then \
		echo "Changes detected. Rebuilding..."; \
		poetry run python transform_zii_blocks.py; \
		touch $(BUILD_TIMESTAMP); \
	else \
		echo "No changes detected. Skipping rebuild."; \
	fi

build: check_changes

serve: build
	mkdocs serve -f mkdocs-dev.yml

deploy: build
	mkdocs gh-deploy --force

clean:
	rm -rf $(PAGES_BUILD_DIR) $(BUILD_TIMESTAMP)
	echo "Cleaned build artifacts."