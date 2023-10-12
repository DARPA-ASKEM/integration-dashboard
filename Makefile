.env:
	cp sample.env .env


PHONY:dev-init
dev-init:.env
	poetry install


PHONY:up
up: .env
	docker build -f docker/Dockerfile -t integration-dashboard .
	docker run --name dashboard -p8501:8501 -e USE_LOCAL='TRUE' -d integration-dashboard


PHONY:down
down:
	docker kill dashboard; docker rm dashboard
