.PHONY: build_docker

DOCKER_IMAGE = butla/contaiwaiter


build_docker:
	docker build -t $(DOCKER_IMAGE) .
