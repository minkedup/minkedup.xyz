all: build

build:
	go tool hugo

watch:
	go tool hugo serve -D

clean:
	rm -rf .hugo_build.lock public/ node_modules/

.PHONY: all build watch clean
