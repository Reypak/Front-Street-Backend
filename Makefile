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