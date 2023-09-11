.env:
	cp sample.env .env

PHONY:init
init:.env
	poetry install
