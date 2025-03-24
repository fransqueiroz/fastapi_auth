.PHONY: help
help:  ## show definitions of all functions
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: run
run:  ## Running the application
	fastapi dev main.py