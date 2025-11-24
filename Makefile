all: build

fmt:
	yarn run prettier -w .

build:
	go tool hugo

watch:
	go tool hugo serve -D

clean:
	rm -rf .hugo_build.lock public/ node_modules/

.PHONY: all fmt build watch clean
