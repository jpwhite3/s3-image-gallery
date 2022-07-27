.PHONY: clean test build bootstrap

clean:
	rm -rf ./dist
	mkdir -p ./dist/images

bootstrap:
	poetry lock && poetry install

test: clean
	cp -R ./src/template/html/* ./dist
	poetry run python ./src/build.py ./test/

build: clean
	cp -R ./src/template/html/* ./dist
	poetry run python ./src/build.py $(GALLERY_DIR)

run: build
	cd ./dist && python3 -m http.server 8000