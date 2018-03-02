# import deploy config
config ?= config.env
include $(config)
export $(shell sed 's/=.*//' $(config))

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# DOCKER TASKS
# Build the container
build: ## Build the container
	@echo
	@echo "----- Building Container -----"
	@echo
	docker build -t $(APP_NAME) .
	@echo
	@echo "----- Container Built -----"
	@echo


build-nc: ## Build the container without caching
	@echo
	@echo "----- Building Container No Cache -----"
	@echo
	docker build --no-cache -t $(APP_NAME) .
	@echo
	@echo "----- Container Built -----"
	@echo

# run: ## Run the addressbook in interactive mode
# 	@echo
# 	@echo "----- Running Interactive -----"
# 	@echo
# 	docker run -it $(APP_NAME) -i

# run-single: ## Does a single address book look up
# 	docker run -it $(APP_NAME)

up: build run ## Build and run the application in interactive mode

test:
	docker run --entrypoint python $(APP_NAME) setup.py "test"
