run:
	python manage.py runserver
test:
	python manage.py test --keepdb thesis

coverage:
	coverage run ./manage.py test --keepdb
	coverage html
