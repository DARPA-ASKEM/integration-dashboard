.env:
	cp sample.env .env


PHONY:dev-init
dev-init:.env
	poetry install


up: .env
	docker build -f docker/Dockerfile -t integration-dashboard .
	docker run --name dashboard -p8501:8501 integration-dashboard

	
