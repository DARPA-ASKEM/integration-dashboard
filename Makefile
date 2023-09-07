
.PHONY:init

init:
	poetry install
	git submodule update --init
	# Install TA1
	cd services/knowledge-middleware
	poetry install
	cd ../..


PHONY: report
report:
	./scripts/ta1.sh
