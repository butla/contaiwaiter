.PHONY: build_docker test run

DOCKER_IMAGE = butla/contaiwaiter


test:
	pytest tests/

build_docker:
	docker build -t $(DOCKER_IMAGE) .

run:
	cd tests; bash -c "docker-compose up --build; docker-compose down -v"
