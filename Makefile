all: build

build:
	go tool hugo

watch:
	go tool hugo serve -D

clean:
	rm -rf .hugo_build.lock public/

.PHONY: all build watch clean
