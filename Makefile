all:
	go tool hugo

clean:
	rm -rf .hugo_build.lock public/

.PHONY: all clean
