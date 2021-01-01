run-frontend:
	cd frontend && npm run serve

run-backend:
	python manage.py runserver

run-test:
	python manage.py test films

run-lint:
	scripts/lint.sh