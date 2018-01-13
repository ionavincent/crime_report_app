docker-run: docker-build
	docker run -it -p 8080:8080 ivincent/flask-example-app:latest

docker-build:
	docker build --squash -f Dockerfile -t ivincent/flask-example-app .
