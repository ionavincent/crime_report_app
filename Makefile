docker-run: docker-build
	docker run -it -p 8080:8080 ivincent/crime-report-app:latest

docker-build:
	docker build --squash -f Dockerfile -t ivincent/crime-report-app .

start-mysql:
	docker run --name crime-report-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7