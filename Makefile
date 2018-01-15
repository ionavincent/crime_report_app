DIR := ${CURDIR}

test:
	nose2

docker-run: docker-build
	docker run -it -e USING_DOCKER=true -v $(DIR):/data ivincent/crime-report-app:latest python -m database.import_crime_reports --zip $(ZIP_FILE)
	docker run -it -e USING_DOCKER=true -v $(DIR):/data -p 8080:8080 ivincent/crime-report-app:latest

docker-build:
	docker build --squash -f Dockerfile -t ivincent/crime-report-app .

start-mysql:
	docker run --name crime-report-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7
