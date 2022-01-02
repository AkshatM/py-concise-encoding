update_antlr:
	docker build . -t antlr:latest

generate:
	docker run --rm -u $(shell id -u ${USER}):$(shell id -g ${USER}) -v $(shell pwd):/work -w="/work" antlr:latest -Dlanguage=Python3 -no-listener -visitor CTELexer.g4 CTE.g4
	rm -rf '?'/
