run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

deploy:
	docker build --platform linux/amd64 -t fs_api .
	docker tag fs_api us-east1-docker.pkg.dev/front-street-ug/app/fs_api
	docker push us-east1-docker.pkg.dev/front-street-ug/app/fs_api
	gcloud run deploy fsapi --image us-east1-docker.pkg.dev/front-street-ug/app/fs_api:latest --region us-east1

push:
	docker push us-east1-docker.pkg.dev/front-street-ug/app/fs_api
	gcloud run deploy fsapi --image us-east1-docker.pkg.dev/front-street-ug/app/fs_api:latest --region us-east1

check-db:
	python manage.py check --database default

save-statement:
	$(info (API) Save sample statement pdf)
	curl http://127.0.0.1:8000/api/loans/statement/1/ > pdfs/sample.pdf