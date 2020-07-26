build:
	@docker build -t tuipik/starnavi_app:latest .
pull:
	@docker pull tuipik/starnavi_app:latest
run:
	@docker-compose up
test:
	@docker-compose run app sh -c "python manage.py test && flake8"