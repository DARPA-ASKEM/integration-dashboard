.env:
	cp sample.env .env

PHONY:init
init:.env
	poetry install
	git submodule update --init
	# Install TA1
	cd services/knowledge-middleware
	poetry install
	cd ../..

PHONY: report
report:
	./scripts/ta1.sh
