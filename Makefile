.PHONY: run
run:
	python manage.py runserver
.PHONY: test
test:
	python manage.py test --keepdb thesis

.PHONY: coverage
coverage:
	coverage run ./manage.py test --keepdb
	coverage html


.PHONY: map
map:
	python scripts/build_map.py

.PHONY: new_map
new_map:
	python scripts/generate_location_info.py
	python scripts/build_map.py



.PHONY: db_map
db_map:
	python manage.py dump_locations
	python scripts/build_map.py
